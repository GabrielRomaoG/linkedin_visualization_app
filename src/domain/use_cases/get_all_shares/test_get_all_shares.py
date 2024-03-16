from datetime import date
import unittest
from unittest.mock import MagicMock
from src.domain.models.shares import Share
from src.domain.use_cases.get_all_shares.get_all_shares import (
    AllSharesGetter,
)
import pandas as pd


class TestAllSharesGetter(unittest.TestCase):
    def setUp(self):
        self.mocked_shares_repository = MagicMock()
        self.use_case = AllSharesGetter(
            shares_repository=self.mocked_shares_repository,
        )

    def test_get_all(self):
        expected_data = [
            {
                "share_link": "https://example.com/share1",
                "shared_date": date(2021, 5, 15),
                "num_of_comments": 10,
                "num_of_reactions": 20,
            },
            {
                "share_link": "https://example.com/share2",
                "shared_date": date(2021, 5, 20),
                "num_of_comments": 5,
                "num_of_reactions": 15,
            },
        ]

        self.mocked_shares_repository.return_value.get_all.return_value = [
            Share(**record) for record in expected_data
        ]
        actual_df = self.use_case.get_all()

        expected_df = pd.DataFrame(expected_data).astype(
            {
                "shared_date": "datetime64[ns]",
            }
        )

        self.assertTrue(expected_df.equals(actual_df))
        self.assertEqual(actual_df["share_link"].dtype, "object")
        self.assertEqual(actual_df["num_of_comments"].dtype, "int64")
        self.assertEqual(actual_df["num_of_reactions"].dtype, "int64")
        self.assertEqual(actual_df["shared_date"].dtype, "datetime64[ns]")
