from sqlalchemy import select, delete
from src.infra.db.settings.connection import DBConnectionHandler
from .connections_repository import ConnectionsRepository
from src.domain.models.connection import Connection as ConnectionModel
from src.infra.db.entities.connections import Connection as ConnectionEntity
from datetime import date
import unittest
import pytest


db_connection_handler = DBConnectionHandler()
db_connection = db_connection_handler.get_engine().connect()


@pytest.mark.skip(reason="Sensive test")
class TestConnectionsRepository(unittest.TestCase):
    def setUp(self):
        self.repository = ConnectionsRepository()

    def test_insert_connection(self):
        mocked_user_name = "teste"
        mocked_company = "some company"
        mocked_position = "Tester Tester"
        mocked_connected_on = date(2023, 10, 12)
        mocked_connection_model = ConnectionModel(
            user_name=mocked_user_name,
            company=mocked_company,
            position=mocked_position,
            connected_on=mocked_connected_on,
        )

        self.repository.insert_connection(mocked_connection_model)

        stmt = select(ConnectionEntity).where(
            ConnectionEntity.user_name == mocked_user_name
        )

        result = db_connection.execute(stmt)
        registry = result.fetchall()[0]

        self.assertEqual(registry.user_name, mocked_user_name)
        self.assertEqual(registry.company, mocked_company)
        self.assertEqual(registry.position, mocked_position)
        self.assertEqual(registry.connected_on, mocked_connected_on)

        del_stmt = delete(ConnectionEntity).where(
            ConnectionEntity.user_name == registry.user_name
        )

        db_connection.execute(del_stmt)
        db_connection.commit()
