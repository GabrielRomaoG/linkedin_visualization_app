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
            logging.error(f"Error fetching webpage '{self.url}': HTTP error {e}")
            raise
        except Exception as e:
            logging.error(
                f"Error fetching or parsing webpage '{self.url}': {e}", exc_info=True
            )
            raise

    def get_num_of_reactions(self) -> Optional[int]:
        if not self.__parsed_html:
            raise ValueError(
                "the html is not fetched and parsed. Please use fetch_and_parse_html first."
            )
        try:

            if self.__parsed_html.find("div", class_="no-content-card"):
                return None

            reactions_html_tag = self.__parsed_html.find(
                "a",
                attrs={
                    "data-tracking-control-name": "public_post_social-actions-reactions"
                },
            )

            num_of_reactions = (
                int(reactions_html_tag.attrs["data-num-reactions"])
                if reactions_html_tag
                else 0
            )

            return num_of_reactions
        except Exception as e:
            logging.error(
                f"Error getting number of reactions of the url '{self.url}': {e}",
                exc_info=True,
            )
            raise

    def get_num_of_comments(self) -> Optional[int]:
        if not self.__parsed_html:
            raise ValueError(
                "the html is not fetched and parsed. Please use fetch_and_parse_html first."
            )
        try:

            if self.__parsed_html.find("div", class_="no-content-card"):
                return None

            comment_html_tag = self.__parsed_html.find(
                "a",
                attrs={
                    "data-tracking-control-name": "public_post_social-actions-comments"
                },
            )

            num_of_comments = (
                int(comment_html_tag.attrs.get("data-num-comments", None))
                if comment_html_tag
                else 0
            )

            return num_of_comments

        except Exception as e:
            logging.error(
                f"Error getting number of reactions of the url '{self.url}': {e}",
                exc_info=True,
            )
            raise
