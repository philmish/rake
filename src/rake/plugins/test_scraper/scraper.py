import requests
from rake.meta_schemas import ScrapeRequest, ScrapedData


class Scraper:
    """
    Scraper Class implementing the methods of the Scraper Protocol from rake.protocols.
    """

    def __init__(
        self,
        req: ScrapeRequest
    ) -> None:
        self.base_url = 'https://httpbin.org/'
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
        body = self.data.json()
        return ScrapedData(
            link=self.target,
            plugin="test_scraper",
            data=body,
            status_code=self.data.status_code,
            response_header=self.data.headers
        )

    def execute(self):
        self.prep()
        self.scrape()
        self.session.close()
        return self.parse()
