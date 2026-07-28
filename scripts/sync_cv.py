"""Synchronize the website's public CV from its authoritative repository."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
import time
import urllib.request
from collections.abc import Callable, Sequence
from http.client import IncompleteRead
from pathlib import Path
from urllib.error import URLError

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_URL = (
    "https://raw.githubusercontent.com/AdvancedImagingUTSW/CV/main/kevin_dean_cv.pdf"
)
DEFAULT_DESTINATION = REPOSITORY_ROOT / "source" / "_static" / "kevin-dean-cv.pdf"
PDF_SIGNATURE = b"%PDF-"


def _download_once(source_url: str, temporary_path: Path, timeout: float) -> None:
    request = urllib.request.Request(
        source_url,
        headers={"User-Agent": "dean-lab-website-cv-sync/1.0"},
    )
    with (
        urllib.request.urlopen(request, timeout=timeout) as response,
        temporary_path.open("wb") as destination,
    ):
        shutil.copyfileobj(response, destination)


def _validate_pdf(path: Path) -> None:
    if path.stat().st_size < len(PDF_SIGNATURE):
        raise ValueError(f"Downloaded CV is empty or truncated: {path}")
    with path.open("rb") as stream:
        signature = stream.read(len(PDF_SIGNATURE))
    if signature != PDF_SIGNATURE:
        raise ValueError(f"Downloaded CV does not begin with the PDF signature: {path}")


def sync_cv(
    source_url: str,
    destination: Path,
    *,
    retries: int = 3,
    timeout: float = 30.0,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Download and atomically install a validated CV PDF."""
    if retries < 1:
        raise ValueError("retries must be at least 1")

    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    os.close(descriptor)
    temporary_path = Path(temporary_name)

    try:
        for attempt in range(retries):
            try:
                _download_once(source_url, temporary_path, timeout)
                _validate_pdf(temporary_path)
                os.replace(temporary_path, destination)
                return
            except (IncompleteRead, URLError, TimeoutError, OSError) as error:
                if attempt + 1 == retries:
                    raise RuntimeError(
                        f"Unable to synchronize CV after {retries} attempts"
                    ) from error
                sleep(float(2**attempt))
    finally:
        temporary_path.unlink(missing_ok=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    parser.add_argument(
        "--destination",
        type=Path,
        default=DEFAULT_DESTINATION,
    )
    arguments = parser.parse_args(argv)

    sync_cv(arguments.source_url, arguments.destination)
    print(f"Synced CV: {arguments.source_url} -> {arguments.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
