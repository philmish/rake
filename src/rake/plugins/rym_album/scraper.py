import requests
from bs4 import BeautifulSoup as soup

from rake.meta_schemas import ScrapeRequest, ScrapedData
from rake.plugins.rym_album.schemas import AlbumBase


class Scraper:
    
    def __init__(
        self,
        req: ScrapeRequest
    ) -> None:
        self.base_url = "https://rateyourmusic.com/"
        self.target = f"{self.base_url}{req.slug}"
        self.req = req

    def prep(self):
        self.session = requests.Session()
        self.request = requests.Request(
            self.req.method.upper(),
            self.target,
            headers=self.req.header
        )
        self.request = self.request.prepare()

    def scrape(self):
        self.data = self.session.send(
            self.request
        )

    def parse(self):
        souped = soup(self.data.content, 'html.parser')

        try:
            
            album = AlbumBase.from_soup(souped)
            return ScrapedData(
                link=self.target,
                plugin="rym_album",
                data=album.dict(),
                status_code=self.data.status_code,
                response_header=self.data.headers
            )
        except Exception as e:
            raise e
            print(e)
            return ScrapedData(
                link=self.target,
                plugin="rym_album",
                data=e,
                status_code=500,
                response_header={"headers": ""}
            )

    def execute(self):
        self.prep()
        self.scrape()
        self.session.close()
        return self.parse()
