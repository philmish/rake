from typing import Dict
from pytest import mark
from fastapi.testclient import TestClient
from rake.server import app
from rake.meta_schemas import ScrapeRequest

client = TestClient(app)

@mark.parametrize(
    "request_data,request_model",
    [
        (
            {"plugin": "test_scraper","slug": "get",},
            ScrapeRequest
            )
        ]
    )
def test_scraper(
    request_data: Dict,
    request_model: ScrapeRequest
    ):
    req = request_model(**request_data)
    resp = client.post(
        "/scrape",
        data=req.json()
        )
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data["status_code"] == 200

    data = resp_data["data"]
    
    for k,v in req.header.items():
        if k in data["headers"]:
            assert data["headers"][k] == v

