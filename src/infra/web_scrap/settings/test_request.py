from src.infra.web_scrap.settings.header_config import http_headers
import requests


def test_request():
    mock_url = (
        "https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A7148829122494885888"
    )
    request = requests.get(mock_url, headers=http_headers)
    assert request.headers["content-type"].split(";")[0] == "text/html"
    assert request.status_code == requests.codes.ok
