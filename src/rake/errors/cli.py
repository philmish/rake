class CLI_Error(Exception):
    """Base exception for CLI errors."""

class UnknownStartMode(CLI_Error):
    """Raised when an unknown mode option is passed to the CLI"""