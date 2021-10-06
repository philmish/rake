from typing import Any, Dict
from rake.meta_schemas import ScrapedData


class ResponseData(ScrapedData):
    data: Dict[str, Any]

