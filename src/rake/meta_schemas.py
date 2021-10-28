from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from pydantic.class_validators import validator
from rake.errors.plugins import PluginValidationError
from rake.errors.scraper import MethodError
from rake.utils.loader import get_submodules
from rake import plugins


class Headers(BaseModel):
    agent: str = "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    referrer: str = "https://google.com"
    accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    encoding: str = "gzip, deflate, br"
    language: str = "en-US,en;q=0.9"

    def dict(self):
        return {
            "User-Agent": self.agent,
            "referrer": self.referrer,
            "Accept": self.accept,
            "Accept-Encoding": self.encoding,
            "Accept-Language": self.language
        }


class ScrapeRequest(BaseModel):
    """Represents the request data to the scrape endpoint."""
    plugin: str
    slug: str
    header: Dict[str, Any] = Field(
        default_factory=lambda: Headers().dict()
        )
    method: str = "GET"
    
    @validator("plugin")
    def validate_plug(cls, v):
        mods = get_submodules(plugins)
        if v not in mods:
            raise PluginValidationError(
                f"{v} is not a valid plugin name."
                )
        return v

    @validator("method")
    def validate_method(cls, v):
        methods = ["GET", "POST", "UPDATE", "DELETE"]
        if v.upper() not in methods:
            raise MethodError(
                f"{v} is not a valid HTTP method (get, post, update, delete)."
            )
        return v


class ScrapedData(BaseModel):
    """Represents the response of the rake api."""
    link: str
    plugin: str
    status_code: int
    response_header: Dict[str,Any]
    timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now()
        )
    data: Any

