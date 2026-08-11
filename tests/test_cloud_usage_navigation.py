from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


def read_doc(name):
    return (SOURCE / name).read_text(encoding="utf-8")


def test_cloud_usage_is_owned_by_lab_resources_navigation_only():
    index = read_doc("index.rst")
    resources = read_doc("resources.rst")

    assert ":doc:`Cloud Usage <cloud-usage>`" not in index
    assert "\n   cloud-usage\n" not in index
    assert ":doc:`cloud-usage`" in resources
    assert "\n   cloud-usage\n" in resources


def test_cloud_usage_is_linked_from_resource_paths():
    expected_links = {
        "resources.rst": ":doc:`cloud-usage`",
        "onboarding.rst": ":doc:`cloud-usage`",
        "working-at-utsw.rst": ":doc:`cloud-usage`",
        "digital-tools.rst": ":doc:`cloud-usage`",
        "data-management.rst": ":doc:`cloud-usage`",
        "departure.rst": ":doc:`cloud-usage`",
    }

    for filename, link in expected_links.items():
        assert link in read_doc(filename)
