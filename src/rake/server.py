from typing import Dict, List
from fastapi import FastAPI, HTTPException
from rake.errors.plugins import PluginError
from rake.errors.scraper import ScraperError
from rake.meta_schemas import ScrapeRequest, ScrapedData

from rake.utils.loader import get_all_plugins, load_plugin

app = FastAPI()

@app.post("/scrape", response_model=ScrapedData)
def scrape(req: ScrapeRequest) -> ScrapedData:
    """
    This endpoint is used as an interface to dynamically load Plugins and execute the loaded Scraper.
    For more information check the Scraper Protocol in the protocols file.
    Dynamic import is handled by a helper function from the utils module.
    """
    try:
        plugin = load_plugin(req.plugin)
        scraper = plugin(req)
    
    except PluginError as e:
        return HTTPException(
            status_code=500,
            detail=f"Failed to load Plugin:\n\n{e}"
        )
    
    try:
        resp = scraper.execute()

    except ScraperError as e:
        return HTTPException(
            status_code=500,
            detail=f"Failed to scrape data:\n\n{e}"
        )

    return resp


@app.get("/rake/plugins", response_model=Dict[str,List[str]])
def get_plugins():
    mods = get_all_plugins()
    return {"plugins": mods}


@app.get("/logs")
def get_logs():
    # TODO implement logging system
    pass