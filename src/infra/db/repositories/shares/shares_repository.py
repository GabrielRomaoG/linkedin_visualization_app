from typing import List, Optional
from src.infra.db.repositories.shares.ishares_repository import (
    ISharesRepository,
)
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.shares import Share as ShareEntity
from src.domain.models.shares import Share as ShareModel


class SharesRepository(ISharesRepository):
    def __init__(self, db_connection_handler=DBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    @staticmethod
    def __entity_to_model(entity: ShareEntity) -> ShareModel:
        return ShareModel(
            share_link=entity.share_link,
            shared_date=entity.shared_date,
            num_of_comments=entity.num_of_comments,
            num_of_likes=entity.num_of_likes,
        )

    @staticmethod
    def __model_to_entity(model: ShareModel) -> ShareEntity:
        return ShareEntity(
            share_link=model.share_link,
            shared_date=model.shared_date,
            num_of_comments=model.num_of_comments,
            num_of_likes=model.num_of_likes,
        )

    def bulk_insert_shares(self, share_models: List[ShareModel]) -> None:
        with self.__db_connection_handler() as database:
            try:
                share_entities = [
                    self.__model_to_entity(model) for model in share_models
                ]
                database.session.add_all(share_entities)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_all(self) -> Optional[List[ShareModel]]:
        with self.__db_connection_handler() as database:
            try:
                share_entities = database.session.query(ShareEntity).all()
                share_models = [
                    self.__entity_to_model(entity) for entity in share_entities
                ]
                return share_models
            except Exception as exception:
                database.session.rollback()
                raise exception
