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
            {"plugin": "test_scraper", "slug": "get"},
            ScrapeRequest
            )
        ]
    )
def test_scraper(request_data: Dict, request_model: ScrapeRequest):
    req = request_model(**request_data)
    resp = client.post(
        "/scrape",
        data=req.json()
        )
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data["status_code"] == 200

    data = resp_data["data"]

    for k, v in req.header.items():
        if k in data["headers"]:
            assert data["headers"][k] == v


@mark.parametrize(
    "request_data, request_model, expectations",
    [
        (
            {"plugin": "imdb_movie", "slug": "title/tt8772262/?ref_=fn_al_tt_1"},
            ScrapeRequest,
            {"title": "Midsommar"}
            )
        ]
    )
def test_imdb_movie(request_data: Dict, request_model: ScrapeRequest, expectations: Dict):
    req = request_model(**request_data)
    resp = client.post(
        "/scrape",
        data=req.json()
    )
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data["status_code"] == 200

    data = resp_data["data"]

    for key, val in expectations.items():
        assert data[key] == val


@mark.parametrize(
    "request_data, request_model, expectations",
    [
        (
            {"plugin": "rym_album", "slug": "release/album/klaus-schulze/irrlicht/"},
            ScrapeRequest,
            {"artist": "Klaus Schulze"}
            )
        ]
    )
def test_rym_album(request_data: Dict[str, str], request_model: ScrapeRequest, expectations: Dict[str, str]):
    req = request_model(**request_data)
    resp = client.post(
        "/scrape",
        data=req.json()
    )
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["status_code"] == 200

    data = resp_data["data"]
    assert len(data["track_list"]) > 0
    assert len(data["track_list"]) == 3

    for key, val in expectations.items():
        assert data[key] == val
