import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "source" / "kevin-dean.rst"
INDEX = ROOT / "source" / "index.rst"
CONF = ROOT / "source" / "conf.py"


def test_kevin_dean_profile_contains_canonical_public_identity():
    text = PROFILE.read_text(encoding="utf-8")

    required = [
        "Kevin M. Dean, Ph.D.",
        "I build open-source, adaptive light-sheet microscopes and image-analysis workflows to reveal rare metastatic colonization events in intact tissues.",
        "Kevin M. Dean develops open-source adaptive microscopy and image-analysis workflows that reveal rare metastatic colonization events in intact tissues and broaden access to advanced imaging.",
        "Assistant Professor",
        "Lyda Hill Department of Bioinformatics",
        "Executive Director, Cancer Cell Imaging Core",
        "Professional positions",
        "Selected publications",
        "Selected tools",
        "Talks and media",
        "Contact",
        "Download public CV",
    ]

    for phrase in required:
        assert phrase in text


def test_kevin_dean_profile_uses_polished_section_labels():
    text = PROFILE.read_text(encoding="utf-8")

    assert "**25-word bio**" not in text
    assert "**100-word bio**" not in text
    assert "**Current title and role**" not in text
    assert "Research thesis" not in text
    assert "Professional positions" in text


def test_research_thesis_leads_selected_publications():
    text = PROFILE.read_text(encoding="utf-8")
    heading = "Selected publications\n====================="
    thesis = (
        "The Dean Lab develops autonomous microscopy, molecular multiplexing, "
        "and content-rich histopathology to identify how cancer cells colonize "
        "distant tissues."
    )
    first_publication = "- Haug J, Galecki S, Lin HY, Wang X, Dean KM."

    assert heading in text
    assert thesis in text
    assert text.index(heading) < text.index(thesis) < text.index(first_publication)


def test_kevin_dean_profile_links_assets_and_structured_data():
    text = PROFILE.read_text(encoding="utf-8")

    required = [
        "_static/kevin-dean-headshot.jpg",
        "_static/kevin-dean-cv.pdf",
        "https://scholar.google.com/citations?user=Uv0B5xIAAAAJ&hl=en",
        "https://orcid.org/0000-0003-0839-2320",
        "https://github.com/thedeanlab/",
        "https://github.com/AdvancedImagingUTSW",
        "https://www.linkedin.com/in/kevin-m-dean/",
        "https://bsky.app/profile/kevin-dean.bsky.social",
        "https://profiles.utsouthwestern.edu/profile/155475/kevin-dean.html",
        '"@type": "ProfilePage"',
        '"@type": "Person"',
        '"sameAs"',
    ]

    for phrase in required:
        assert phrase in text


def test_kevin_dean_profile_is_linked_and_css_is_enabled():
    index = INDEX.read_text(encoding="utf-8")
    config = runpy.run_path(CONF)

    assert ":doc:`Kevin Dean <kevin-dean>`" in index
    assert "kevin-dean" in index
    assert config["html_static_path"] == ["_static"]
    assert set(config["html_css_files"]) == {
        "profile.css",
        "meetings.css",
        "publications.css",
    }


def test_index_uses_compact_site_directory_instead_of_wiki_sections():
    index = INDEX.read_text(encoding="utf-8")

    assert "Wiki Sections" not in index
    assert "Explore the site through the public resources below." in index
    assert ".. container:: site-directory" in index
    for link in [
        ":doc:`Repositories <repositories>`",
        ":doc:`Kevin Dean <kevin-dean>`",
        ":doc:`Teaching <teaching>`",
        ":doc:`Publications <publications>`",
        ":doc:`Lab Resources <resources>`",
    ]:
        assert link in index

    assert index.index("   repositories") < index.index("   kevin-dean")
