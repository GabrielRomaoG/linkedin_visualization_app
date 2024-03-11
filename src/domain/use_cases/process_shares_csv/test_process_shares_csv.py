from datetime import date
import unittest
from unittest.mock import MagicMock, mock_open, patch
from src.domain.models.shares import Share
from src.domain.use_cases.process_shares_csv.process_shares_csv import (
    SharesCsvProcessor,
)
import pytest


class TestSharesCsvProcessor(unittest.TestCase):
    def setUp(self):
        self.mocked_shares_repository = MagicMock()
        self.use_case = SharesCsvProcessor(
            shares_repository=self.mocked_shares_repository,
        )

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_error__validate_file_name(self):
        mocked_file_name = "test.csv"
        mocked_file_path = f"some/path/{mocked_file_name}"

        with self.assertRaises(Exception) as context:
            self.use_case.process(mocked_file_path)

        self.assertEqual(
            str(context.exception),
            f"File name '{mocked_file_name}' does not match the interest file name 'Shares.csv'",
        )

    def test__open(self):
        mocked_file_path = "some/place/Shares.csv"
        mock_file_content = (
            "Date,ShareLink,ShareCommentary,SharedURL,MediaURL,Visibility"
        )
        with patch.object(
            self.use_case,
            "_SharesCsvProcessor__open_file",
            mock_open(read_data=mock_file_content),
        ):
            self.use_case.process(mocked_file_path)
            self.use_case._SharesCsvProcessor__open_file.assert_called_once_with(
                mocked_file_path, "r"
            )

    def test_error_is_valid_connections_csv(self):
        mocked_file_path = "some/place/Shares.csv"
        mock_file_content = (
            "Date,ShareLink,ShareCommentary,SharedURL2323,MediaURL,Visibility"
        )
        with patch.object(
            self.use_case,
            "_SharesCsvProcessor__open_file",
            mock_open(read_data=mock_file_content),
        ):
            with self.assertRaises(Exception) as context:
                self.use_case.process(mocked_file_path)

            self.assertEqual(
                str(context.exception),
                "Shares.csv doesn't have the expected columns",
            )
            self.use_case._SharesCsvProcessor__shares_repository.bulk_insert_shares.assert_not_called()

    def test_error_index_equal_5_and_not_valid_csv(self):
        mocked_file_path = "some/place/Shares.csv"
        mock_file_content = (
            "\n\n\n\n\n\n\nDate,ShareLink,ShareCommentary,SharedURL,MediaURL,Visibility"
        )
        with patch.object(
            self.use_case,
            "_SharesCsvProcessor__open_file",
            mock_open(read_data=mock_file_content),
        ):
            with self.assertRaises(Exception) as context:
                self.use_case.process(mocked_file_path)

            self.assertEqual(
                str(context.exception),
                "Shares.csv doesn't have the expected columns",
            )
            self.use_case._SharesCsvProcessor__shares_repository.bulk_insert_shares.assert_not_called()

    def test__process_success(self):
        mocked_file_path = "some/place/Shares.csv"
        mocked_file_content = (
            "Date,ShareLink,ShareCommentary,SharedURL,MediaURL,Visibility\n"
            "2024-01-05 00:14:41,linkedin/link/test1,'Some thing',,,MEMBER_NETWORK\n"
            "2024-04-12 12:14:41,linkedin/link/test2,'Some thing2',,,MEMBER_NETWORK\n"
        )
        with patch.object(
            self.use_case,
            "_SharesCsvProcessor__open_file",
            mock_open(read_data=mocked_file_content),
        ):
            expected_call_to_bulk_insert_connections = [
                Share(
                    share_link="linkedin/link/test1",
                    shared_date=date(2024, 1, 5),
                    num_of_comments=10,
                    num_of_reactions=40,
                ),
                Share(
                    share_link="linkedin/link/test2",
                    shared_date=date(2024, 4, 12),
                    num_of_comments=10,
                    num_of_reactions=40,
                ),
            ]
            self.use_case.process(mocked_file_path)
            self.use_case._SharesCsvProcessor__shares_repository().bulk_insert_shares.assert_called_once_with(
                expected_call_to_bulk_insert_connections
            )

    def test_warning_empty_url(self):
        mocked_file_path = "some/place/Shares.csv"
        mocked_file_content = (
            "Date,ShareLink,ShareCommentary,SharedURL,MediaURL,Visibility\n"
            "2024-01-05 00:14:41,,,,,"
        )
        with patch.object(
            self.use_case,
            "_SharesCsvProcessor__open_file",
            mock_open(read_data=mocked_file_content),
        ):

            self.use_case.process(mocked_file_path)
            log = self._caplog.records[0]
            self.assertEqual(
                log.message,
                "The ShareLink in the row 0 of the table is empty, so it will not be processed.",
            )
            self.assertEqual(log.levelname, "WARNING")
            self.use_case._SharesCsvProcessor__shares_repository.bulk_insert_shares.assert_not_called()
