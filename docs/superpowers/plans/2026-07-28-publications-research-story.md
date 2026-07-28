# Publications Research Story Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the placeholder publications page with the approved Build → Scale → Discover research narrative and guarantee that each production website deployment publishes the latest validated CV from `AdvancedImagingUTSW/CV`.

**Architecture:** Keep the page as hand-authored reStructuredText because its value is editorial selection and interpretation, while treating NCBI My Bibliography, Google Scholar, and ORCID as the comprehensive records. Add a page-specific stylesheet through the existing Sphinx static-asset mechanism. Isolate CV retrieval and validation in a small standard-library Python command that GitHub Actions runs before Sphinx, leaving a synchronized committed PDF as the local/offline fallback.

**Tech Stack:** Sphinx 5.x, reStructuredText, `sphinx_rtd_theme`, CSS, Python 3.9+ standard library, pytest, GitHub Actions

## Global Constraints

- The page must follow the approved continuous editorial layout, not a card grid.
- The research arc and visible section order are **Build → Scale → Discover**.
- Use the ten approved representative publications and their PubMed destinations.
- Do not display full author lists, DOI strings, PMIDs, abstracts, citation counts, or h-index values.
- Describe collaborative biological studies without implying that all work was solely lab-led.
- NCBI My Bibliography, Google Scholar, ORCID, and the stable website CV path are the complete-record destinations.
- The authoritative CV is `AdvancedImagingUTSW/CV@main:kevin_dean_cv.pdf`.
- A production build must fail rather than silently publish the committed fallback when CV synchronization fails.
- Preserve the existing Read the Docs typography and blue-gray palette.
- Added UI must be keyboard accessible, use descriptive links, avoid color-only meaning, and meet WCAG AA contrast.
- Validate approved wording through specification review, a warning-free Sphinx build, and rendered-page inspection.
- Do not add tests that assert exact prose fragments.
- Preserve unrelated work and the existing untracked `tmp/` directory.

---

## File Map

- Create `scripts/sync_cv.py`: download, validate, and atomically install the authoritative CV.
- Create `tests/test_sync_cv.py`: exercise CV validation, atomic replacement, and retry behavior without network access.
- Modify `.github/workflows/static.yml`: synchronize the CV before every production Sphinx build.
- Modify `source/_static/kevin-dean-cv.pdf`: store the current upstream PDF as the local/offline fallback.
- Modify `source/publications.rst`: contain the approved editorial narrative and record links.
- Modify `source/index.rst`: preserve `Publications` as the hidden-toctree navigation label.
- Create `source/_static/publications.css`: style the narrative, publication entries, record links, and closing inset.
- Modify `source/conf.py`: register `publications.css`.
- Modify `tests/test_kevin_dean_profile.py`: extend the existing structural stylesheet-registration assertion; do not add prose assertions.

---

### Task 1: Add Validated CV Synchronization

**Files:**
- Create: `scripts/sync_cv.py`
- Create: `tests/test_sync_cv.py`
- Modify: `.github/workflows/static.yml`
- Modify: `source/_static/kevin-dean-cv.pdf`

**Interfaces:**
- Consumes: public raw PDF at `https://raw.githubusercontent.com/AdvancedImagingUTSW/CV/main/kevin_dean_cv.pdf`
- Produces: `sync_cv(source_url: str, destination: pathlib.Path, *, retries: int = 3, timeout: float = 30.0, sleep: Callable[[float], None] = time.sleep) -> None`
- Produces: CLI `python3 scripts/sync_cv.py [--source-url URL] [--destination PATH]`
- Produces: a validated PDF at `source/_static/kevin-dean-cv.pdf`

- [ ] **Step 1: Write behavior tests for valid, invalid, and transient downloads**

Create `tests/test_sync_cv.py`:

```python
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


def test_sync_cv_rejects_non_pdf_without_replacing_existing_file(
    tmp_path, monkeypatch
):
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
```

- [ ] **Step 2: Run the targeted tests and confirm that the module is missing**

Run:

```bash
pytest tests/test_sync_cv.py -v
```

Expected: collection fails because `scripts.sync_cv` does not yet exist.

- [ ] **Step 3: Implement the standard-library synchronization command**

Create `scripts/sync_cv.py`:

```python
"""Synchronize the website's public CV from its authoritative repository."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
import time
import urllib.request
from collections.abc import Callable, Sequence
from pathlib import Path
from urllib.error import URLError


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "AdvancedImagingUTSW/CV/main/kevin_dean_cv.pdf"
)
DEFAULT_DESTINATION = (
    REPOSITORY_ROOT / "source" / "_static" / "kevin-dean-cv.pdf"
)
PDF_SIGNATURE = b"%PDF-"


def _download_once(source_url: str, temporary_path: Path, timeout: float) -> None:
    request = urllib.request.Request(
        source_url,
        headers={"User-Agent": "dean-lab-website-cv-sync/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        with temporary_path.open("wb") as destination:
            shutil.copyfileobj(response, destination)


def _validate_pdf(path: Path) -> None:
    if path.stat().st_size < len(PDF_SIGNATURE):
        raise ValueError(f"Downloaded CV is empty or truncated: {path}")
    with path.open("rb") as stream:
        signature = stream.read(len(PDF_SIGNATURE))
    if signature != PDF_SIGNATURE:
        raise ValueError(
            f"Downloaded CV does not begin with the PDF signature: {path}"
        )


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
            except (URLError, TimeoutError, OSError) as error:
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
```

- [ ] **Step 4: Run targeted tests and static checks**

Run:

```bash
pytest tests/test_sync_cv.py -v
ruff check scripts/sync_cv.py tests/test_sync_cv.py
```

Expected: three tests pass and Ruff reports no errors.

- [ ] **Step 5: Synchronize the committed fallback from the authoritative repository**

Run:

```bash
python3 scripts/sync_cv.py
curl --fail --location --retry 3 \
  --output /tmp/authoritative-kevin-dean-cv.pdf \
  https://raw.githubusercontent.com/AdvancedImagingUTSW/CV/main/kevin_dean_cv.pdf
shasum -a 256 \
  source/_static/kevin-dean-cv.pdf \
  /tmp/authoritative-kevin-dean-cv.pdf
```

Expected: both SHA-256 hashes are identical, and the command reports the source
and destination paths.

- [ ] **Step 6: Add the synchronization gate to the production workflow**

In `.github/workflows/static.yml`, insert this step after `Setup Python 3.9` and
before `Install Dependencies`:

```yaml
      - name: Synchronize latest public CV
        run: python3 scripts/sync_cv.py
```

This ordering ensures every deployment refreshes and validates the CV before
dependency installation or Sphinx compilation. An exception from the command
must terminate the job.

- [ ] **Step 7: Verify the workflow file and rerun the synchronization tests**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

import yaml

workflow = Path(".github/workflows/static.yml")
data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
steps = data["jobs"]["deploy"]["steps"]
names = [step.get("name") for step in steps]
sync_index = names.index("Synchronize latest public CV")
build_index = names.index("Build HTML with Sphinx")
assert steps[sync_index]["run"] == "python3 scripts/sync_cv.py"
assert sync_index < build_index
print("CV synchronization precedes the Sphinx build.")
PY
pytest tests/test_sync_cv.py -v
```

Expected: the script prints the ordering confirmation and all three tests pass.

- [ ] **Step 8: Commit the CV synchronization unit**

Run:

```bash
git add \
  scripts/sync_cv.py \
  tests/test_sync_cv.py \
  .github/workflows/static.yml \
  source/_static/kevin-dean-cv.pdf
git commit -m "build: synchronize latest public CV"
```

Expected: one commit containing only the synchronization command, its behavioral
tests, workflow integration, and the updated fallback PDF.

---

### Task 2: Write the Build → Scale → Discover Narrative

**Files:**
- Modify: `source/publications.rst`
- Modify: `source/index.rst`

**Interfaces:**
- Consumes: approved copy and PubMed destinations from `docs/superpowers/specs/2026-07-28-publications-research-story-design.md`
- Produces: semantic reStructuredText containers named `publication-lead`, `publication-record-summary`, `publication-record-links`, `publication-list`, `publication-entry`, `publication-meta`, and `publication-record-inset`
- Produces: the visible page heading `Our Research Story`
- Produces: the hidden-toctree label `Publications`

- [ ] **Step 1: Replace the placeholder with the approved editorial content**

Replace `source/publications.rst` with:

```rst
Our Research Story
==================

.. container:: publication-lead

   Modern biological imaging often forces a trade-off between resolution,
   scale, adaptability, and accessibility. Our research program works across
   that boundary: we build open and adaptive light-sheet microscopes, scale
   them from subcellular dynamics to intact tissues, and use them with
   collaborators to discover how cells and organs are organized and function.

.. container:: publication-record-summary

   This page presents a curated view rather than a comprehensive bibliography.
   For the complete record, use the sources below.

   .. container:: publication-record-links

      `NCBI My Bibliography <https://www.ncbi.nlm.nih.gov/myncbi/kevin.dean.1/bibliography/public/>`__
      `Google Scholar <https://scholar.google.com/citations?user=Uv0B5xIAAAAJ&hl=en>`__
      `ORCID <https://orcid.org/0000-0003-0839-2320>`__
      `Curriculum vitae <_static/kevin-dean-cv.pdf>`__

Build Open and Adaptive Imaging Systems
---------------------------------------

Advanced microscopy is most useful when strong optical performance is paired
with accessibility, open control, adaptable sample geometry, and reproducible
operation.

.. container:: publication-list

   .. container:: publication-entry

      **`A versatile oblique plane microscope for large-scale and
      high-resolution imaging of subcellular dynamics
      <https://pubmed.ncbi.nlm.nih.gov/33179596/>`__**

      .. container:: publication-meta

         *eLife, 2020*

      Combined high-numerical-aperture optics with a versatile sample geometry
      to support high-resolution imaging across cells, embryos, and tissue
      sections.

   .. container:: publication-entry

      **`Navigate: an open-source platform for smart light-sheet microscopy
      <https://pubmed.ncbi.nlm.nih.gov/39261640/>`__**

      .. container:: publication-meta

         *Nature Methods, 2024*

      Created an open control platform that turns light-sheet microscopes into
      programmable systems for intelligent and adaptive acquisition.

   .. container:: publication-entry

      **`Mechanically sheared axially swept light-sheet microscopy
      <https://pubmed.ncbi.nlm.nih.gov/39296406/>`__**

      .. container:: publication-meta

         *Biomedical Optics Express, 2024*

      Placed acquired data directly into its spatial context while enlarging
      the field of view and reducing interpolation-heavy post-processing.

   .. container:: publication-entry

      **`A high-resolution, easy-to-build light-sheet microscope for
      subcellular imaging <https://pubmed.ncbi.nlm.nih.gov/41642252/>`__**

      .. container:: publication-meta

         *eLife, 2026*

      Paired simplified alignment and open-source control with subcellular
      resolution, lowering the practical barrier to high-performance
      light-sheet imaging.

Scale from Cells to Whole Tissues
---------------------------------

Biological mechanisms span spatial scales, but conventional imaging often
forces a choice between detailed local measurements and the tissue context in
which those measurements matter.

.. container:: publication-list

   .. container:: publication-entry

      **`Light-sheet microscopy of cleared tissues with isotropic, subcellular
      resolution <https://pubmed.ncbi.nlm.nih.gov/31673159/>`__**

      .. container:: publication-meta

         *Nature Methods, 2019*

      Brought isotropic subcellular resolution to millimeter-scale cleared
      tissues across diverse immersion media.

   .. container:: publication-entry

      **`Isotropic imaging across spatial scales with axially swept
      light-sheet microscopy <https://pubmed.ncbi.nlm.nih.gov/35831614/>`__**

      .. container:: publication-meta

         *Nature Protocols, 2022*

      Made ASLM reproducible across expanded samples, living cells, and cleared
      organisms through detailed build guidance, operating procedures, and
      software.

   .. container:: publication-entry

      **`Feature-driven whole-tissue imaging with subcellular resolution
      <https://pubmed.ncbi.nlm.nih.gov/40902591/>`__**

      .. container:: publication-meta

         *Cell Reports Methods, 2025*

      Combined centimeter-scale survey imaging with targeted high-resolution
      interrogation, concentrating acquisition on rare or informative biology.

Discover Biological Mechanisms
------------------------------

The instrumentation is not an endpoint. Its value is demonstrated through
biological collaborations that connect molecular organization and cell
morphology to cell behavior and whole-organ function.

.. container:: publication-list

   .. container:: publication-entry

      **`Pre-complexation of talin and vinculin without tension is required for
      efficient nascent adhesion maturation
      <https://pubmed.ncbi.nlm.nih.gov/33783351/>`__**

      .. container:: publication-meta

         *eLife, 2021*

      Showed that talin and vinculin must assemble before mechanical loading
      for efficient maturation of nascent adhesions.

   .. container:: publication-entry

      **`Blebs promote cell survival by assembling oncogenic signalling hubs
      <https://pubmed.ncbi.nlm.nih.gov/36859545/>`__**

      .. container:: publication-meta

         *Nature, 2023*

      Used three-dimensional imaging to reveal blebs as signaling hubs that
      support anoikis resistance in melanoma cells.

   .. container:: publication-entry

      **`An epithelial morphogenetic program for maximal urine concentration
      <https://pubmed.ncbi.nlm.nih.gov/41862496/>`__**

      .. container:: publication-meta

         *Nature Communications, 2026*

      Integrated transcriptomics and high-resolution imaging to connect
      ascending thin-limb epithelial architecture with whole-organ
      urine-concentrating function.

.. container:: publication-record-inset

   **Explore the complete publication record**

   This page presents a curated research narrative rather than a comprehensive
   bibliography. Browse NCBI My Bibliography, Google Scholar, ORCID, or the
   full CV for the complete record.

   .. container:: publication-record-links

      `NCBI My Bibliography <https://www.ncbi.nlm.nih.gov/myncbi/kevin.dean.1/bibliography/public/>`__
      `Google Scholar <https://scholar.google.com/citations?user=Uv0B5xIAAAAJ&hl=en>`__
      `ORCID <https://orcid.org/0000-0003-0839-2320>`__
      `Curriculum vitae <_static/kevin-dean-cv.pdf>`__
```

- [ ] **Step 2: Preserve the Publications navigation label**

In the hidden toctree in `source/index.rst`, change:

```rst
   publications
```

to:

```rst
   Publications <publications>
```

This keeps the sidebar label `Publications` while allowing the document's visible
heading to be `Our Research Story`.

- [ ] **Step 3: Review the source directly against the approved specification**

Run:

```bash
git diff -- source/publications.rst source/index.rst
git diff --check -- source/publications.rst source/index.rst
```

Confirm manually:

- the visible heading is `Our Research Story`;
- Build, Scale, and Discover appear once and in that order;
- there are exactly ten `publication-entry` containers;
- every title, venue/year, annotation, and destination matches the approved
  specification;
- the only complete-record destinations are My Bibliography, Google Scholar,
  ORCID, and the stable CV path;
- there are no citation metrics, full author lists, DOI strings, visible PMIDs,
  or abstract excerpts.
- the hidden toctree uses `Publications <publications>`.

- [ ] **Step 4: Build the unstyled document with warnings treated as errors**

Run:

```bash
validation_dir="$(mktemp -d /tmp/dean-publications-content.XXXXXX)"
sphinx-build -W --keep-going -b html source "$validation_dir"
```

Expected: Sphinx reports `build succeeded` with no warnings. The temporary path
is intentionally outside `build/` to avoid stale-output false positives.

- [ ] **Step 5: Commit the approved narrative**

Run:

```bash
git add source/publications.rst source/index.rst
git commit -m "docs: tell the lab publication story"
```

Expected: one content-only commit containing the approved editorial narrative.

---

### Task 3: Add Scannable, Accessible Editorial Styling

**Files:**
- Create: `source/_static/publications.css`
- Modify: `source/conf.py:66`
- Modify: `tests/test_kevin_dean_profile.py:80-87`

**Interfaces:**
- Consumes: the seven `publication-*` container classes defined in Task 2
- Produces: Sphinx registration `html_css_files = ["profile.css", "meetings.css", "publications.css"]`
- Produces: responsive styling at the existing `760px` breakpoint

- [ ] **Step 1: Extend the existing structural stylesheet test**

Change the assertion in
`test_kevin_dean_profile_is_linked_and_css_is_enabled` to:

```python
    assert set(config["html_css_files"]) == {
        "profile.css",
        "meetings.css",
        "publications.css",
    }
```

Do not add assertions for narrative phrases or publication titles.

- [ ] **Step 2: Run the structural test and confirm that registration is missing**

Run:

```bash
pytest \
  tests/test_kevin_dean_profile.py::test_kevin_dean_profile_is_linked_and_css_is_enabled \
  -v
```

Expected: failure shows that `publications.css` is absent from
`html_css_files`.

- [ ] **Step 3: Register the page-specific stylesheet**

Change `source/conf.py` to:

```python
html_static_path = ["_static"]
html_css_files = ["profile.css", "meetings.css", "publications.css"]
```

- [ ] **Step 4: Implement the editorial CSS**

Create `source/_static/publications.css`:

```css
.publication-lead {
  color: #334e5f;
  font-size: 1.08rem;
  line-height: 1.65;
  margin: 0.8rem 0 1.1rem;
}

.publication-lead p:last-child,
.publication-record-summary p:last-child,
.publication-record-links p:last-child,
.publication-entry p:last-child,
.publication-record-inset p:last-child {
  margin-bottom: 0;
}

.publication-record-summary {
  border-bottom: 1px solid #d9e2ec;
  margin-bottom: 1.8rem;
  padding-bottom: 1.25rem;
}

.publication-record-links {
  margin-top: 0.75rem;
}

.publication-record-links > p {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0;
}

.publication-record-links a {
  background: #ffffff;
  border: 1px solid #c9d6e2;
  border-radius: 4px;
  color: #24527a;
  display: inline-block;
  font-weight: 600;
  padding: 0.38rem 0.58rem;
}

.publication-list {
  margin: 0.8rem 0 2rem;
}

.publication-entry {
  border-top: 1px solid #d9e2ec;
  padding: 1rem 0;
}

.publication-entry:first-child {
  border-top: 0;
  padding-top: 0.25rem;
}

.publication-entry > p:first-child {
  font-size: 1.02rem;
  line-height: 1.45;
  margin-bottom: 0.25rem;
}

.publication-entry .publication-meta {
  color: #526675;
  font-size: 0.94rem;
  margin-bottom: 0.45rem;
}

.publication-entry .publication-meta p {
  margin: 0;
}

.publication-record-inset {
  background: #f7f9fb;
  border: 1px solid #d9e2ec;
  border-radius: 6px;
  margin: 2rem 0 1rem;
  padding: 1.1rem 1.2rem;
}

.publication-record-inset > p:first-child {
  color: #1f2d3d;
  font-size: 1.08rem;
  margin-bottom: 0.45rem;
}

@media screen and (max-width: 760px) {
  .publication-lead {
    font-size: 1rem;
  }

  .publication-record-links > p {
    align-items: stretch;
    flex-direction: column;
  }

  .publication-record-links a {
    width: 100%;
  }

  .publication-record-inset {
    padding: 1rem;
  }
}
```

- [ ] **Step 5: Run the structural test and CSS checks**

Run:

```bash
pytest \
  tests/test_kevin_dean_profile.py::test_kevin_dean_profile_is_linked_and_css_is_enabled \
  -v
git diff --check -- \
  source/conf.py \
  source/_static/publications.css \
  tests/test_kevin_dean_profile.py
```

Expected: the targeted test passes and `git diff --check` emits no output.

- [ ] **Step 6: Build the styled page from a fresh output directory**

Run:

```bash
validation_dir="$(mktemp -d /tmp/dean-publications-styled.XXXXXX)"
sphinx-build -W --keep-going -b html source "$validation_dir"
test -f "$validation_dir/publications.html"
test -f "$validation_dir/_static/publications.css"
```

Expected: warning-free Sphinx success and both output files exist.

- [ ] **Step 7: Commit the stylesheet and registration**

Run:

```bash
git add \
  source/_static/publications.css \
  source/conf.py \
  tests/test_kevin_dean_profile.py
git commit -m "style: add publications editorial layout"
```

Expected: one commit containing the page-specific CSS, Sphinx registration, and
the structural stylesheet assertion only.

---

### Task 4: Perform Full Specification and Rendered-Page Validation

**Files:**
- Verify: `source/publications.rst`
- Verify: `source/_static/publications.css`
- Verify: `source/_static/kevin-dean-cv.pdf`
- Verify: `.github/workflows/static.yml`
- Verify: rendered `publications.html`, `kevin-dean.html`, and `repositories.html`

**Interfaces:**
- Consumes: all deliverables from Tasks 1–3
- Produces: a warning-free, visually inspected Sphinx artifact and an evidence-backed completion report

- [ ] **Step 1: Run the complete automated suite and Python quality checks**

Run:

```bash
pytest -v
ruff check scripts/sync_cv.py tests/test_sync_cv.py
git diff --check "$(git merge-base HEAD origin/protocols)"..HEAD
```

Expected: the complete pytest suite passes, Ruff reports no errors, and the diff
check emits no output.

- [ ] **Step 2: Build the complete site with warnings treated as errors**

Run:

```bash
python3 scripts/sync_cv.py
validation_dir="$(mktemp -d /tmp/dean-publications-final.XXXXXX)"
printf '%s\n' "$validation_dir" > /tmp/dean-publications-final.path
sphinx-build -W --keep-going -b html source "$validation_dir"
```

Expected: `build succeeded` with no warnings.

- [ ] **Step 3: Verify every selected-paper and complete-record destination**

Run:

```bash
python3 - <<'PY'
import time
from pathlib import Path
from urllib.request import Request, urlopen

html = Path("source/publications.rst").read_text(encoding="utf-8")
urls = [
    "https://pubmed.ncbi.nlm.nih.gov/33179596/",
    "https://pubmed.ncbi.nlm.nih.gov/39261640/",
    "https://pubmed.ncbi.nlm.nih.gov/39296406/",
    "https://pubmed.ncbi.nlm.nih.gov/41642252/",
    "https://pubmed.ncbi.nlm.nih.gov/31673159/",
    "https://pubmed.ncbi.nlm.nih.gov/35831614/",
    "https://pubmed.ncbi.nlm.nih.gov/40902591/",
    "https://pubmed.ncbi.nlm.nih.gov/33783351/",
    "https://pubmed.ncbi.nlm.nih.gov/36859545/",
    "https://pubmed.ncbi.nlm.nih.gov/41862496/",
    "https://www.ncbi.nlm.nih.gov/myncbi/kevin.dean.1/bibliography/public/",
    "https://scholar.google.com/citations?user=Uv0B5xIAAAAJ&hl=en",
    "https://orcid.org/0000-0003-0839-2320",
]
for url in urls:
    assert url in html, url
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        assert 200 <= response.status < 400, (url, response.status)
    print(f"OK {url}")
    time.sleep(0.4)
PY
```

If Google Scholar returns rate limiting while the other destinations succeed,
open the exact Scholar profile URL in the browser and verify the visible profile
name instead of weakening or removing the link. `BeautifulSoup` is available
through the project dependency set; its import also confirms the environment
used for site validation is active.

- [ ] **Step 4: Verify the authoritative and published CV bytes**

Run:

```bash
validation_dir="$(cat /tmp/dean-publications-final.path)"
curl --fail --location --retry 3 \
  --output /tmp/authoritative-kevin-dean-cv.pdf \
  https://raw.githubusercontent.com/AdvancedImagingUTSW/CV/main/kevin_dean_cv.pdf
shasum -a 256 \
  source/_static/kevin-dean-cv.pdf \
  "$validation_dir/_static/kevin-dean-cv.pdf" \
  /tmp/authoritative-kevin-dean-cv.pdf
```

Expected: all three hashes are identical.

- [ ] **Step 5: Inspect the rendered publications page at desktop width**

Serve the fresh artifact:

```bash
validation_dir="$(cat /tmp/dean-publications-final.path)"
python3 -m http.server 8765 --directory "$validation_dir"
```

Using the in-app browser, open
`http://127.0.0.1:8765/publications.html` at approximately `1440 × 900` and
inspect the complete page.

Confirm:

- the page reads as one continuous editorial narrative;
- the lead and complete-record links are visible without dominating the page;
- Build, Scale, and Discover have strong but restrained hierarchy;
- all ten paper titles, venue lines, and annotations are legible;
- dividers and spacing make entries scannable without producing card-like blocks;
- the closing inset is visually distinct but subordinate to the narrative;
- keyboard focus remains visible on every link;
- no text, border, or link relies on color alone.

- [ ] **Step 6: Inspect responsive behavior and neighboring pages**

At approximately `390 × 844`, verify that:

- record-link buttons stack without horizontal overflow;
- long publication titles wrap cleanly;
- publication annotations remain readable;
- the closing inset stays within the viewport;
- the site navigation remains usable.

Then inspect:

- `http://127.0.0.1:8765/kevin-dean.html`
- `http://127.0.0.1:8765/repositories.html`

Confirm that the additional stylesheet introduces no visible regressions.

- [ ] **Step 7: Review the implementation against every specification section**

Open
`docs/superpowers/specs/2026-07-28-publications-research-story-design.md` and
compare it with the source and rendered output. Record evidence for:

- purpose and audience;
- all goals and non-goals;
- opening thesis and record links;
- ten approved publication entries;
- closing complete-record inset;
- visual and accessibility constraints;
- CV authority and failure behavior;
- relationship to the profile and Repositories pages;
- every validation and success criterion.

If any check fails, stop, correct the responsible earlier task in a narrowly
scoped commit, and rerun Task 4 from Step 1.

- [ ] **Step 8: Request final code and specification review**

Use `superpowers:requesting-code-review` with:

- base commit: the implementation branch point;
- head commit: the current implementation head;
- requirements: the approved design specification;
- verification evidence: pytest, Ruff, warning-free Sphinx output, link checks,
  CV hash comparison, desktop inspection, and mobile inspection.

Address any substantive findings with focused commits and repeat the affected
verification steps before reporting completion.
