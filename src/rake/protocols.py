from typing import Protocol

class Scraper(Protocol):

    def prep(self):
        """Called before the web request."""

    def scrape(self):
        """Executes the prepared web request to aquire data."""

    def parse(self):
        """Parses recieved response."""

    def execute(self):
        """Executes prep, scrape and parse and sets additional context if needed."""
