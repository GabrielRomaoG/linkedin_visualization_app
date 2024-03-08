from sqlalchemy import select, delete
from src.infra.db.test_resources.connection_handler_test_class import (
    DBConnectionHandler as DBConnectionHandlerTest,
)
from src.infra.db.repositories.shares.shares_repository import (
    SharesRepository,
)
from src.infra.db.entities.shares import Share as ShareEntity
from src.domain.models.shares import Share as ShareModel
from datetime import date
import unittest


class TestSharesRepository(unittest.TestCase):
    def setUp(self):
        DBConnectionHandlerTest.build_db()
        self.repository = SharesRepository(DBConnectionHandlerTest)

    @classmethod
    def tearDown(cls) -> None:
        DBConnectionHandlerTest.delete_db()

    def test_bulk_insert_shares(self):
        mocked_share_links = ["linked/test4", "linked/test5", "linked/test6"]
        mocked_share_models = [
            ShareModel(
                share_link=id,
                shared_date=date(2023, 10, 12),
                num_of_comments=10,
                num_of_likes=50,
            )
            for id in mocked_share_links
        ]

        self.repository.bulk_insert_shares(mocked_share_models)

        db_handler = DBConnectionHandlerTest().get_engine().connect()

        stmt = select(ShareEntity).where(ShareEntity.share_link.in_(mocked_share_links))
        result = db_handler.execute(stmt).fetchall()

        self.assertEqual(len(result), len(mocked_share_links))

        for model, entity in zip(mocked_share_models, result):
            self.assertEqual(entity.share_link, model.share_link)
            self.assertEqual(entity.shared_date, model.shared_date)
            self.assertEqual(entity.num_of_comments, model.num_of_comments)
            self.assertEqual(entity.num_of_likes, model.num_of_likes)

        del_stmt = delete(ShareEntity).where(
            ShareEntity.share_link.in_(mocked_share_links)
        )
        db_handler.execute(del_stmt)
        db_handler.commit()

    def test_get_all_shares(self):

        repository_result = self.repository.get_all()

        db_handler = DBConnectionHandlerTest().get_engine().connect()

        stmt = select(ShareEntity)
        query_result = db_handler.execute(stmt).fetchall()

        use_case_result_length = len(repository_result)
        self.assertEqual(len(query_result), use_case_result_length)

        for repository_record, query_result_record in zip(
            repository_result, query_result
        ):
            self.assertEqual(
                repository_record.share_link, query_result_record.share_link
            )
            self.assertEqual(
                repository_record.shared_date, query_result_record.shared_date
            )
            self.assertEqual(
                repository_record.num_of_comments, query_result_record.num_of_comments
            )
            self.assertEqual(
                repository_record.num_of_likes, query_result_record.num_of_likes
            )
