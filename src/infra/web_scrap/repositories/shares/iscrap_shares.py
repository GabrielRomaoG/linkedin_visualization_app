from abc import ABC, abstractmethod
from typing import Optional
from bs4 import BeautifulSoup


class ISharesScrapper(ABC):
    """
    Defines an interface for scraping webpage content and extracting specific information.
    """

    @abstractmethod
    def set_url(self, url: str) -> None:
        """
        Sets the URL of the webpage to be scraped.

        Args:
            url (str): The URL of the webpage.

        Raises:
            ValueError: If the provided URL is invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_and_parse_html(self) -> Optional[BeautifulSoup]:
        """
        Fetches the webpage content, parses it, and returns the BeautifulSoup object.

        Returns:
            Optional[BeautifulSoup]: The parsed HTML content or None if an error occurs.
        """
        raise NotImplementedError

    @abstractmethod
    def get_num_of_reactions(self) -> int:
        """
        Extracts the number of reactions from the parsed HTML content.

        Raises:
            ValueError: If the HTML content hasn't been fetched and parsed.

        Returns:
            int: The number of reactions on the webpage.
        """
        raise NotImplementedError

    @abstractmethod
    def get_num_of_comments(self) -> int:
        """
        Extracts the number of comments from the parsed HTML content.

        Raises:
            ValueError: If the HTML content hasn't been fetched and parsed.

        Returns:
            int: The number of comments on the webpage.
        """
        raise NotImplementedError
