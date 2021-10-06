import importlib
import pkgutil
from typing import List
from rake.errors.plugins import PluginLoadingError
from rake.protocols import Scraper


def get_submodules(module) -> List [str]:
    """Returns the list of submodules for a given module."""
    res = []
    for plug in pkgutil.iter_modules(module.__path__):
        res.append(plug.name)
    return res


def load_plugin(_import: str) -> Scraper:
    """Helper function to dynamically import plugins."""
    try:
        mod = importlib.import_module(
            f"rake.plugins.{_import}.scraper"
            )
        return getattr(mod, 'Scraper')
    
    except Exception as e:
        raise PluginLoadingError(
            f"{e}\n\nCould not load {_import}\n\n"
            )


