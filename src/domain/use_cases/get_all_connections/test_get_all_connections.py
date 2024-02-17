from datetime import date
import unittest
from unittest.mock import MagicMock
from src.domain.models.connection import Connection
from src.domain.use_cases.get_all_connections.get_all_connections import (
    AllConnectionsGetter,
)
import pandas as pd


class TestAllConnectionsGetter(unittest.TestCase):
    def setUp(self):
        self.mocked_connections_repository = MagicMock()
        self.use_case = AllConnectionsGetter(
            connections_repository=self.mocked_connections_repository,
        )

    def test_get_all(self):
        expected_data = [
            {
                "user_name": "john_doe",
                "company": "MicroTest",
                "position": "Tester",
                "connected_on": date(2016, 1, 12),
            },
            {
                "user_name": "alice2a",
                "company": "Test C",
                "position": "Teacher",
                "connected_on": date(2017, 10, 22),
            },
        ]

        self.mocked_connections_repository.return_value.get_all.return_value = [
            Connection(**record) for record in expected_data
        ]
        actual_df = self.use_case.get_all()

        expected_df = pd.DataFrame(expected_data)

        self.assertTrue(expected_df.equals(actual_df))
