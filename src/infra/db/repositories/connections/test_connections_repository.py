from sqlalchemy import select, delete
from src.infra.db.test_resources.connection_handler_test_class import (
    DBConnectionHandler as DBConnectionHandlerTest,
)
from src.infra.db.repositories.connections.connections_repository import (
    ConnectionsRepository,
)
from src.domain.models.connection import Connection as ConnectionModel
from src.infra.db.entities.connections import Connection as ConnectionEntity
from datetime import date
import unittest


class TestConnectionsRepository(unittest.TestCase):
    def setUp(self):
        DBConnectionHandlerTest.build_db()
        self.repository = ConnectionsRepository(DBConnectionHandlerTest)

    @classmethod
    def tearDown(cls) -> None:
        DBConnectionHandlerTest.delete_db()

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

        db_handler = DBConnectionHandlerTest().get_engine().connect()

        stmt = select(ConnectionEntity).where(
            ConnectionEntity.user_name == mocked_user_name
        )
        result = db_handler.execute(stmt).fetchall()
        registry = result[0]

        self.assertEqual(registry.user_name, mocked_user_name)
        self.assertEqual(registry.company, mocked_company)
        self.assertEqual(registry.position, mocked_position)
        self.assertEqual(registry.connected_on, mocked_connected_on)

        del_stmt = delete(ConnectionEntity).where(
            ConnectionEntity.user_name == registry.user_name
        )

        db_handler.execute(del_stmt)
        db_handler.commit()

    def test_bulk_insert_connections(self):
        mocked_user_names = ["test1", "test2", "test3"]
        mocked_connection_models = [
            ConnectionModel(
                user_name=name,
                company="Test Company",
                position="Tester",
                connected_on=date(2023, 10, 12),
            )
            for name in mocked_user_names
        ]

        self.repository.bulk_insert_connections(mocked_connection_models)

        db_handler = DBConnectionHandlerTest().get_engine().connect()

        stmt = select(ConnectionEntity).where(
            ConnectionEntity.user_name.in_(mocked_user_names)
        )
        result = db_handler.execute(stmt).fetchall()

        self.assertEqual(len(result), len(mocked_user_names))

        for model, entity in zip(mocked_connection_models, result):
            self.assertEqual(entity.user_name, model.user_name)
            self.assertEqual(entity.company, model.company)
            self.assertEqual(entity.position, model.position)
            self.assertEqual(entity.connected_on, model.connected_on)

        del_stmt = delete(ConnectionEntity).where(
            ConnectionEntity.user_name.in_(mocked_user_names)
        )
        db_handler.execute(del_stmt)
        db_handler.commit()

    def test_get_all(self):

        use_case_result = self.repository.get_all()

        db_handler = DBConnectionHandlerTest().get_engine().connect()

        stmt = select(ConnectionEntity)
        query_result = db_handler.execute(stmt).fetchall()

        use_case_result_length = len(use_case_result)
        self.assertEqual(len(query_result), use_case_result_length)

        for use_case_record, query_result_record in zip(use_case_result, query_result):
            self.assertEqual(use_case_record.user_name, query_result_record.user_name)
            self.assertEqual(use_case_record.company, query_result_record.company)
            self.assertEqual(use_case_record.position, query_result_record.position)
            self.assertEqual(
                use_case_record.connected_on, query_result_record.connected_on
            )
