import unittest
from unittest.mock import MagicMock
from bs4 import BeautifulSoup
from src.infra.web_scrap.repositories.shares.scrap_shares import SharesScrapper
import requests


class TestSharesScrapper(unittest.TestCase):
    def setUp(self) -> None:
        self.mocked_http_headers = {"User-Agent": "My Custom User Agent"}
        self.mocked_http_library = MagicMock()
        self.repository = SharesScrapper(
            request_library=self.mocked_http_library,
            http_headers=self.mocked_http_headers,
        )

    def test_set_url_with_invalid_url_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            self.repository.set_url("https://www.invalidurl.com")
        self.assertTrue("The url provided is not valid" in str(context.exception))

    def test_fetch_and_parse_html_without_url_set_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            self.repository.fetch_and_parse_html()
        self.assertTrue("URL is not set" in str(context.exception))

    def test_fetch_and_parse_html_http_error_raises_http_error(self):
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.mocked_http_library.get.side_effect = requests.HTTPError("HTTP Error")
        with self.assertRaises(requests.HTTPError) as context:
            self.repository.fetch_and_parse_html()
        self.assertTrue("HTTP Error" in str(context.exception))

    def test_fetch_and_parse_html_success(self):
        mock_url = "https://www.linkedin.com/feed/update/test123123"
        with open("src/infra/web_scrap/test_resources/share.html", "r") as file:
            mocked_html_content = file.read()
        self.mocked_http_library.get.return_value.text = mocked_html_content
        self.mocked_http_library.get.return_value.raise_for_status.return_value = None

        self.repository.set_url(mock_url)
        self.repository.fetch_and_parse_html()

        self.mocked_http_library.get.assert_called_once_with(
            url=mock_url, headers=self.mocked_http_headers
        )
        self.assertEqual(
            self.repository._SharesScrapper__parsed_html,
            BeautifulSoup(mocked_html_content, "html.parser"),
        )

    def test_get_num_of_reactions_without_fetching_html_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            self.repository.get_num_of_reactions()
        self.assertTrue("the html is not fetched and parsed" in str(context.exception))

    def test_get_num_of_comments_without_fetching_html_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            self.repository.get_num_of_comments()
        self.assertTrue("the html is not fetched and parsed" in str(context.exception))

    def test_get_num_of_reactions_no_content_share(self):
        with open(
            "src/infra/web_scrap/test_resources/no_content_share.html", "r"
        ) as file:
            mocked_html_content = file.read()
        self.mocked_http_library.get.return_value.text = mocked_html_content
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.repository.fetch_and_parse_html()
        num_of_reactions = self.repository.get_num_of_reactions()
        self.assertIsNone(num_of_reactions)

    def test_get_num_of_reactions_none_tag(self):
        self.mocked_http_library.get.return_value.text = ""
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.repository.fetch_and_parse_html()
        num_of_reactions = self.repository.get_num_of_reactions()
        self.assertIsInstance(num_of_reactions, int)
        self.assertEqual(num_of_reactions, 0)

    def test_get_num_of_reactions_success(self):
        with open("src/infra/web_scrap/test_resources/share.html", "r") as file:
            mocked_html_content = file.read()
        self.mocked_http_library.get.return_value.text = mocked_html_content
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.repository.fetch_and_parse_html()
        num_of_reactions = self.repository.get_num_of_reactions()
        self.assertIsInstance(num_of_reactions, int)
        self.assertEqual(num_of_reactions, 116)

    def test_get_num_of_comments_no_content_share(self):
        with open(
            "src/infra/web_scrap/test_resources/no_content_share.html", "r"
        ) as file:
            mocked_html_content = file.read()
        self.mocked_http_library.get.return_value.text = mocked_html_content
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.repository.fetch_and_parse_html()
        num_of_comments = self.repository.get_num_of_comments()
        self.assertIsNone(num_of_comments)

    def test_get_num_of_comments_none_tag(self):
        self.mocked_http_library.get.return_value.text = ""
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.repository.fetch_and_parse_html()
        num_of_comments = self.repository.get_num_of_comments()
        self.assertIsInstance(num_of_comments, int)
        self.assertEqual(num_of_comments, 0)

    def test_get_num_of_comments_success(self):
        with open("src/infra/web_scrap/test_resources/share.html", "r") as file:
            mocked_html_content = file.read()
        self.mocked_http_library.get.return_value.text = mocked_html_content
        self.repository.set_url("https://www.linkedin.com/feed/update/test123123")
        self.repository.fetch_and_parse_html()
        num_of_comments = self.repository.get_num_of_comments()
        self.assertIsInstance(num_of_comments, int)
        self.assertEqual(num_of_comments, 23)
