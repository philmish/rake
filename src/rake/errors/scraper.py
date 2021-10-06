class ScraperError(Exception):
    """Base Exception for all scraper errors."""

class MethodError(ScraperError):
    """Raised when an unknown method is passed with a Request."""