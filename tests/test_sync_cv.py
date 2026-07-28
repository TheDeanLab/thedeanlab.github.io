from io import BytesIO
from urllib.error import URLError

import pytest

from scripts import sync_cv


class Response(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def test_sync_cv_atomically_replaces_destination_after_valid_download(
    tmp_path, monkeypatch
):
    destination = tmp_path / "kevin-dean-cv.pdf"
    destination.write_bytes(b"%PDF-old")
    downloaded = b"%PDF-1.7\nnew cv"

    def fake_urlopen(request, timeout):
        assert request.full_url == "https://example.test/cv.pdf"
        assert timeout == 7.0
        return Response(downloaded)

    monkeypatch.setattr(sync_cv.urllib.request, "urlopen", fake_urlopen)

    sync_cv.sync_cv(
        "https://example.test/cv.pdf",
        destination,
        retries=1,
        timeout=7.0,
    )

    assert destination.read_bytes() == downloaded
    assert list(tmp_path.glob(".kevin-dean-cv.pdf.*.tmp")) == []


def test_sync_cv_rejects_non_pdf_without_replacing_existing_file(tmp_path, monkeypatch):
    destination = tmp_path / "kevin-dean-cv.pdf"
    destination.write_bytes(b"%PDF-existing")

    monkeypatch.setattr(
        sync_cv.urllib.request,
        "urlopen",
        lambda request, timeout: Response(b"<html>not a pdf</html>"),
    )

    with pytest.raises(ValueError, match="PDF signature"):
        sync_cv.sync_cv(
            "https://example.test/cv.pdf",
            destination,
            retries=1,
        )

    assert destination.read_bytes() == b"%PDF-existing"
    assert list(tmp_path.glob(".kevin-dean-cv.pdf.*.tmp")) == []


def test_sync_cv_retries_transient_network_errors(tmp_path, monkeypatch):
    destination = tmp_path / "kevin-dean-cv.pdf"
    attempts = 0
    delays = []

    def fake_urlopen(request, timeout):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise URLError("temporary failure")
        return Response(b"%PDF-1.7\nretried cv")

    monkeypatch.setattr(sync_cv.urllib.request, "urlopen", fake_urlopen)

    sync_cv.sync_cv(
        "https://example.test/cv.pdf",
        destination,
        retries=3,
        sleep=delays.append,
    )

    assert attempts == 3
    assert delays == [1.0, 2.0]
    assert destination.read_bytes() == b"%PDF-1.7\nretried cv"
