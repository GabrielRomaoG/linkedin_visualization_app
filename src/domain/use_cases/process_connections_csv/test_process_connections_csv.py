from datetime import date
import unittest
from unittest.mock import MagicMock, mock_open, patch
from src.domain.models.connection import Connection
from src.domain.use_cases.process_connections_csv.process_connections_csv import (
    ConnectionsCsvProcessor,
)
import pytest


class TestConnectionsCsvProcessor(unittest.TestCase):
    def setUp(self):
        self.mocked_connections_repository = MagicMock()
        self.mocked_os_get_env = MagicMock()
        self.use_case = ConnectionsCsvProcessor(
            connections_repository=self.mocked_connections_repository,
            os_get_env=self.mocked_os_get_env,
        )

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog: pytest.LogCaptureFixture):
        self._caplog = caplog

    def test_error__validate_file_name(self):
        mocked_file_name = "test.csv"
        mocked_file_path = f"some/path/{mocked_file_name}"

        with self.assertRaises(Exception) as context:
            self.use_case.process(mocked_file_path)

        self.assertEqual(
            str(context.exception),
            f"File name '{mocked_file_name}' does not match the interest file name 'Connections.csv'",
        )

    def test__open(self):
        mocked_file_path = "some/place/Connections.csv"
        mock_file_content = (
            "First Name,Last Name,Company,URL,Email Address,Position,Connected On"
        )
        with patch.object(
            self.use_case,
            "_ConnectionsCsvProcessor__open_file",
            mock_open(read_data=mock_file_content),
        ):
            self.use_case.process(mocked_file_path)
            self.use_case._ConnectionsCsvProcessor__open_file.assert_called_once_with(
                mocked_file_path, "r"
            )

    def test_error_is_valid_connections_csv(self):
        mocked_file_path = "some/place/Connections.csv"
        mock_file_content = (
            "First Name,Last Name,Company,URL,something,Email Address,Position"
        )
        with patch.object(
            self.use_case,
            "_ConnectionsCsvProcessor__open_file",
            mock_open(read_data=mock_file_content),
        ):
            with self.assertRaises(Exception) as context:
                self.use_case.process(mocked_file_path)

            self.assertEqual(
                str(context.exception),
                "Connections.csv doesn't have the expected columns",
            )
            self.use_case._ConnectionsCsvProcessor__connections_repository.bulk_insert_connections.assert_not_called()

    def test_error_index_equal_5_and_not_valid_csv(self):
        mocked_file_path = "some/place/Connections.csv"
        mock_file_content = "\n\n\n\n\n\n\nFirst Name,Last Namennnn,Company,URL12434,Email Address,Position,Connected On"
        with patch.object(
            self.use_case,
            "_ConnectionsCsvProcessor__open_file",
            mock_open(read_data=mock_file_content),
        ):
            with self.assertRaises(Exception) as context:
                self.use_case.process(mocked_file_path)

            self.assertEqual(
                str(context.exception),
                "Connections.csv doesn't have the expected columns",
            )
            self.use_case._ConnectionsCsvProcessor__connections_repository.bulk_insert_connections.assert_not_called()

    def test__get_env_condition_not_local(self):
        mocked_file_path = "some/place/Connections.csv"
        mocked_file_content = (
            "First Name,Last Name,Company,URL,Email Address,Position,Connected On\n"
            "John,Doe,MicroTest,www.example.com/johndoe,johndoe@test.com,Tester,01 Jan 2012\n"
            "Alice,Waht,Testbook,www.lnk.com/alicew,alicew@some.com,Designer,24 Feb 2016"
        )
        self.mocked_os_get_env.side_effect = lambda arg: (
            "web" if arg == "ENVIRONMENT" else None
        )
        with patch.object(
            self.use_case,
            "_ConnectionsCsvProcessor__open_file",
            mock_open(read_data=mocked_file_content),
        ):
            expected_result = [
                Connection(
                    user_name="johndoe",
                    company="MicroTest",
                    position="Tester",
                    connected_on=date(2012, 1, 1),
                ),
                Connection(
                    user_name="alicew",
                    company="Testbook",
                    position="Designer",
                    connected_on=date(2016, 2, 24),
                ),
            ]
            result = self.use_case.process(mocked_file_path)
            self.use_case._ConnectionsCsvProcessor__connections_repository().bulk_insert_connections.assert_not_called()
            self.assertEqual(result, expected_result)

    def test__process_success(self):
        mocked_file_path = "some/place/Connections.csv"
        mocked_file_content = (
            "First Name,Last Name,Company,URL,Email Address,Position,Connected On\n"
            "John,Doe,MicroTest,www.example.com/johndoe,johndoe@test.com,Tester,01 Jan 2012\n"
            "Alice,Waht,Testbook,www.lnk.com/alicew,alicew@some.com,Designer,24 Feb 2016"
        )
        self.mocked_os_get_env.side_effect = lambda arg: (
            "local" if arg == "ENVIRONMENT" else None
        )
        with patch.object(
            self.use_case,
            "_ConnectionsCsvProcessor__open_file",
            mock_open(read_data=mocked_file_content),
        ):
            expected_call_to_bulk_insert_connections = [
                Connection(
                    user_name="johndoe",
                    company="MicroTest",
                    position="Tester",
                    connected_on=date(2012, 1, 1),
                ),
                Connection(
                    user_name="alicew",
                    company="Testbook",
                    position="Designer",
                    connected_on=date(2016, 2, 24),
                ),
            ]
            result = self.use_case.process(mocked_file_path)
            self.use_case._ConnectionsCsvProcessor__connections_repository().bulk_insert_connections.assert_called_once_with(
                expected_call_to_bulk_insert_connections
            )
            self.assertEqual(result, expected_call_to_bulk_insert_connections)

    def test_warning_empty_url(self):
        mocked_file_path = "some/place/Connections.csv"
        mocked_file_content = (
            "First Name,Last Name,Company,URL,Email Address,Position,Connected On\n"
            ",,,,,,01 Jan 2012"
        )
        with patch.object(
            self.use_case,
            "_ConnectionsCsvProcessor__open_file",
            mock_open(read_data=mocked_file_content),
        ):

            self.use_case.process(mocked_file_path)
            log = self._caplog.records[0]
            self.assertEqual(
                log.message,
                "The URL in the row 0 of the table is empty, so it will not be processed.",
            )
            self.assertEqual(log.levelname, "WARNING")
            self.use_case._ConnectionsCsvProcessor__connections_repository.bulk_insert_connections.assert_not_called()
