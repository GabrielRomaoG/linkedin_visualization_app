import pandas as pd
import unittest
from unittest.mock import MagicMock
from src.domain.use_cases.process_connections_csv.process_connections_csv import (
    ConnectionsCsvProcessor,
)


class TestConnectionsCsvProcessor(unittest.TestCase):
    def setUp(self):
        self.mocked_read_csv = MagicMock()
        self.use_case = ConnectionsCsvProcessor(read_csv_func=self.mocked_read_csv)

    def test_process(self):
        mocked_file_path = "some/place/Connections.csv"
        self.mocked_read_csv.return_value = pd.DataFrame(
            {
                "First Name": ["John", "Jane"],
                "Last Name": ["Doe", "Smith"],
                "Company": ["ABC Inc.", "XYZ Corp."],
                "URL": ["www.example.com/johndoe", "www.example.com/janesmith"],
                "Email Address": ["john@example.com", "jane@example.com"],
                "Position": ["Manager", "Engineer"],
                "Connected On": ["01 Jan 2022", "15 Feb 2022"],
            }
        )

        result = self.use_case.process(mocked_file_path)

        self.assertEqual(len(self.mocked_read_csv.return_value), len(result))
        self.assertEqual(
            result.Company.values, self.mocked_read_csv.return_value.Company.values
        )
        self.assertEqual(
            result.Position.values, self.mocked_read_csv.return_value.Position.values
        )

    def test__validate_file_name(self):
        mocked_file_name = "test.csv"
        mocked_file_path = f"some/path/{mocked_file_name}"

        with self.assertRaises(Exception) as context:
            self.use_case.process(mocked_file_path)

        self.assertEqual(
            str(context.exception),
            f"File name '{mocked_file_name}' does not match the interest file name 'Connections.csv'",
        )

    def test__read_connections_csv(self):
        mocked_file_path = "some/place/Connections.csv"
        self.mocked_read_csv.return_value = pd.DataFrame(
            {
                "First Name": ["John", "Jane"],
                "Last Name": ["Doe", "Smith"],
                "Company": ["ABC Inc.", "XYZ Corp."],
                "URL": ["www.example.com/johndoe", "www.example.com/janesmith"],
                "Email Address": ["john@example.com", "jane@example.com"],
                "Position": ["Manager", "Engineer"],
                "Connected On": ["01 Jan 2022", "15 Feb 2022"],
            }
        )

        result = self.use_case.process(mocked_file_path)

        self.assertIsInstance(result, pd.DataFrame)

    def test__validate_columns(self):
        mocked_file_path = "some/place/Connections.csv"
        self.mocked_read_csv.return_value = pd.DataFrame(
            {
                "First Name": ["John", "Jane"],
                "Company2323": ["ABC Inc.", "XYZ Corp."],
                "URL": ["www.example.com/johndoe", "www.example.com/janesmith"],
                "Email Address": ["john@example.com", "jane@example.com"],
                "Position": ["Manager", "Engineer"],
                "Connected On": ["01 Jan 2022", "15 Feb 2022"],
            }
        )

        with self.assertRaises(Exception) as context:
            self.use_case.process(mocked_file_path)
        self.assertEqual(
            str(context.exception),
            "DataFrame does not contain all expected columns",
        )

    def test__set_data_types(self):
        mocked_file_path = "some/place/Connections.csv"
        self.mocked_read_csv.return_value = pd.DataFrame(
            {
                "First Name": ["John", "Jane"],
                "Last Name": ["Doe", "Smith"],
                "Company": ["ABC Inc.", "XYZ Corp."],
                "URL": ["www.example.com/johndoe", "www.example.com/janesmith"],
                "Email Address": ["john@example.com", "jane@example.com"],
                "Position": ["Manager", "Engineer"],
                "Connected On": ["01 Jan 2022", "15 Feb 2022"],
            }
        )

        result = self.use_case.process(mocked_file_path)

        self.assertEqual(result["Company"].dtype, "string")
        self.assertEqual(result["Position"].dtype, "string")
        self.assertEqual(result["Connected On"].dtype, "datetime64[ns]")

    def test__create_user_name_column(self):
        mocked_file_path = "some/place/Connections.csv"
        self.mocked_read_csv.return_value = pd.DataFrame(
            {
                "First Name": ["John", "Jane"],
                "Last Name": ["Doe", "Smith"],
                "Company": ["ABC Inc.", "XYZ Corp."],
                "URL": ["www.example.com/johndoe", "www.example.com/janesmith"],
                "Email Address": ["john@example.com", "jane@example.com"],
                "Position": ["Manager", "Engineer"],
                "Connected On": ["01 Jan 2022", "15 Feb 2022"],
            }
        )

        result = self.use_case.process(mocked_file_path)

        self.assertIn("user_name", result.columns)
        self.assertEqual("johndoe", result["user_name"].values[0])
        self.assertEqual("janesmith", result["user_name"].values[1])

    def test__select_interest_columns(self):
        mocked_file_path = "some/place/Connections.csv"
        self.mocked_read_csv.return_value = pd.DataFrame(
            {
                "First Name": ["John", "Jane"],
                "Last Name": ["Doe", "Smith"],
                "Company": ["ABC Inc.", "XYZ Corp."],
                "URL": ["www.example.com/johndoe", "www.example.com/janesmith"],
                "Email Address": ["john@example.com", "jane@example.com"],
                "Position": ["Manager", "Engineer"],
                "Connected On": ["01 Jan 2022", "15 Feb 2022"],
            }
        )

        result = self.use_case.process(mocked_file_path)

        self.assertListEqual(
            list(result.columns), ["user_name", "Company", "Position", "Connected On"]
        )
