import unittest
from unittest.mock import MagicMock
from streamlit.testing.v1 import AppTest
from src.presentation.streamlit_pages.shares import SharesPage
import pandas as pd
import pandas.testing as pdt


class TestSharesPage(unittest.TestCase, AppTest):
    def setUp(self) -> None:
        self.page_path = "src/presentation/streamlit_pages/shares.py"
        self.mocked_all_shares_getter = MagicMock()
        self.page = SharesPage(all_shares_getter=self.mocked_all_shares_getter)
        self.mocked_all_shares_df = pd.DataFrame(
            {
                "shared_date": pd.date_range(start="2023-01-01", periods=4, freq="M"),
                "num_of_reactions": [100, 150, 200, 250],
                "num_of_comments": [10, 15, 20, 25],
            }
        )
        self.mocked_all_shares_getter.return_value.get_all.return_value = (
            self.mocked_all_shares_df
        )

    def test__generate_shares_by_month_year_df(self):
        expected_result = pd.DataFrame(
            {
                "month_year": [
                    "Jan-2023",
                    "Feb-2023",
                    "Mar-2023",
                    "Apr-2023",
                ],
                "count": [1, 1, 1, 1],
            }
        )

        result = SharesPage._SharesPage__generate_shares_by_month_year_df(
            self.mocked_all_shares_df.copy()
        )
        result_sorted = result.sort_values(by="month_year").reset_index(drop=True)
        expected_result_sorted = expected_result.sort_values(
            by="month_year"
        ).reset_index(drop=True)

        pdt.assert_frame_equal(result_sorted, expected_result_sorted)

    def test_streamlit_success_run(self):
        page_run = self.from_file(self.page_path).run()
        self.assertEqual(len(page_run.exception), 0)
