import pytest
from rake.errors.plugins import PluginLoadingError
from rake.utils.loader import load_plugin


@pytest.mark.parametrize("name", ["test_scraper"])
def test_plugin_loader(name: str):
    expectation = f"rake.plugins.{name}.scraper"
    scraper = load_plugin(name)
    assert scraper.__module__ == expectation

    wrong = name[::-1]
    with pytest.raises(PluginLoadingError):
        _ = load_plugin(wrong)
