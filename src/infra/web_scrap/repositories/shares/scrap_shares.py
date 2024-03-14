from typing import Optional
import requests
import logging
from src.infra.web_scrap.repositories.shares.iscrap_shares import ISharesScrapper
from src.infra.web_scrap.settings.header_config import http_headers
from bs4 import BeautifulSoup


class SharesScrapper(ISharesScrapper):
    def __init__(self, request_library=requests, http_headers=http_headers):
        self.__request_library = request_library
        self.__http_headers = http_headers
        self.url: Optional[str] = None
        self.__parsed_html: Optional[BeautifulSoup] = None

    def set_url(self, url: str) -> None:
        expected_url_start = "https://www.linkedin.com/feed/update/"
        if not url.startswith(expected_url_start):
            raise ValueError(
                f"The url provided is not valid, must start with {expected_url_start}"
            )
        self.url = url
        return self

    def fetch_and_parse_html(self) -> BeautifulSoup:
        if not self.url:
            raise ValueError("URL is not set. Please use set_url(url) first.")

        try:
            response = self.__request_library.get(
                url=self.url, headers=self.__http_headers
            )
            response.raise_for_status()

            self.__parsed_html = BeautifulSoup(response.text, "html.parser")
            return self

        except requests.HTTPError as e:
            logging.error(f"Error fetching webpage: HTTP error {e}")
            raise
        except Exception as e:
            logging.error(f"Error fetching or parsing webpage: {e}", exc_info=True)
            raise

    def get_num_of_reactions(self) -> int:
        if not self.__parsed_html:
            raise ValueError(
                "the html is not fetched and parsed. Please use fetch_and_parse_html first."
            )
        num_of_reactions = int(
            self.__parsed_html.find(
                "a",
                attrs={
                    "data-tracking-control-name": "public_post_social-actions-reactions"
                },
            ).attrs["data-num-reactions"]
        )

        return num_of_reactions

    def get_num_of_comments(self) -> int:
        if not self.__parsed_html:
            raise ValueError(
                "the html is not fetched and parsed. Please use fetch_and_parse_html first."
            )
        num_of_comments = int(
            self.__parsed_html.find(
                "a",
                attrs={
                    "data-tracking-control-name": "public_post_social-actions-comments"
                },
            ).attrs["data-num-comments"]
        )

        return num_of_comments
