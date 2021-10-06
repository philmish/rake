class PluginError(Exception):
    """Base exception for all Plugin errors."""


class PluginLoadingError(PluginError):
    """Raised when the loader failes to import a plugin."""


class PluginValidationError(PluginError):
    """Raised when a plugin name cant be validated by a pydantic model."""