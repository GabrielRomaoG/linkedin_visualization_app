import unittest
from unittest.mock import MagicMock
from streamlit.testing.v1 import AppTest
from src.presentation.streamlit_pages.connections import ConnectionsPage
import pandas as pd
import pandas.testing as pdt


class TestConnectionsPage(unittest.TestCase, AppTest):
    def setUp(self) -> None:
        self.page_path = "src/presentation/streamlit_pages/connections.py"
        self.mocked_all_connections_getter = MagicMock()
        self.mocked_job_mapper = {
            "Data Analyst": ["Data Analyst", "analista de dados"],
            "Recruiter": ["Recruiter", "Tech Recruiter"],
        }
        self.page = ConnectionsPage(
            all_connections_getter=self.mocked_all_connections_getter,
            job_position_mapper=self.mocked_job_mapper,
        )
        self.mocked_all_connections_df = pd.DataFrame(
            {
                "user_name": ["teste1", "teste2", "teste3", "teste4"],
                "company": ["TST", "ADV", "ADV", "IRIM"],
                "position": [
                    "Analista de dados",
                    "Data Scientist",
                    "Tech Recruiter",
                    "Data Analyst",
                ],
                "connected_on": pd.Series(
                    ["2023-02-15", "2023-02-15", "2023-03-05", "2023-03-05"],
                    dtype="datetime64[ns]",
                ),
            }
        )
        self.mocked_all_connections_getter.return_value.get_all.return_value = (
            self.mocked_all_connections_df
        )

    def test__generate_weekly_count_connections_df(self):
        expected_result = pd.DataFrame(
            {
                "week_year": [
                    "07-2023",
                    "08-2023",
                    "09-2023",
                    "10-2023",
                ],
                "count": [2, 0, 0, 2],
            }
        ).reset_index(drop=True)

        result = self.page._ConnectionsPage__generate_weekly_count_connections_df(
            self.mocked_all_connections_df.copy()
        ).reset_index(drop=True)

        pdt.assert_frame_equal(result, expected_result)

    def test__generate_positions_count_df(self):
        expected_result = pd.Series(
            data=[2, 1, 1],
            index=pd.Index(
                [
                    "Data Analyst",
                    "Recruiter",
                    "Other",
                ],
                name="mapped_position",
            ),
        )

        result = self.page._ConnectionsPage__generate_positions_count_df(
            self.mocked_all_connections_df.copy(), self.mocked_job_mapper
        )
        result_sorted = result.sort_index()
        expected_result_sorted = expected_result.sort_index()

        pdt.assert_series_equal(result_sorted, expected_result_sorted)

    def test__generate_recruiter_proportion_df(self):
        expected_result = {
            "is_recruiter": [
                False,
                True,
            ],
            "count": [3, 1],
        }

        result = self.page._ConnectionsPage__generate_recruiter_proportion_df(1, 4)

        self.assertDictEqual(result, expected_result)

    def test__generate_companies_count(self):
        expected_result = (
            pd.DataFrame({"company": ["ADV", "IRIM", "TST"], "count": [2, 1, 1]})
            .sort_values(by="company")
            .reset_index(drop=True)
        )

        result = (
            self.page._ConnectionsPage__generate_companies_count(
                self.mocked_all_connections_df, 10
            )
            .sort_values(by="company")
            .reset_index(drop=True)
        )

        pdt.assert_frame_equal(expected_result, result)

    def test_streamlit_success_run(self):
        page_run = self.from_file(self.page_path).run()
        self.assertEqual(len(page_run.exception), 0)
