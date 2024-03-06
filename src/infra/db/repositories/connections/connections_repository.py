from typing import List, Optional
from src.infra.db.repositories.connections.iconnections_repository import (
    IConnectionsRepository,
)
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.connections import Connection as ConnectionEntity
from src.domain.models.connection import Connection as ConnectionModel


class ConnectionsRepository(IConnectionsRepository):
    def __init__(self, db_connection_handler=DBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    @staticmethod
    def __entity_to_model(entity: ConnectionEntity) -> ConnectionModel:
        return ConnectionModel(
            user_name=entity.user_name,
            company=entity.company,
            position=entity.position,
            connected_on=entity.connected_on,
        )

    @staticmethod
    def __model_to_entity(model: ConnectionModel) -> ConnectionEntity:
        return ConnectionEntity(
            user_name=model.user_name,
            company=model.company,
            position=model.position,
            connected_on=model.connected_on,
        )

    def insert_connection(self, connections_model: ConnectionModel) -> None:
        new_registry = self.__model_to_entity(connections_model)
        with self.__db_connection_handler() as database:
            try:
                database.session.add(new_registry)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def bulk_insert_connections(
        self, connections_models: List[ConnectionModel]
    ) -> None:
        with self.__db_connection_handler() as database:
            try:
                connections_entities = [
                    self.__model_to_entity(model) for model in connections_models
                ]
                database.session.add_all(connections_entities)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_all(self) -> Optional[List[ConnectionModel]]:
        with self.__db_connection_handler() as database:
            try:
                connections_entities = database.session.query(ConnectionEntity).all()
                connections_models = [
                    self.__entity_to_model(connection)
                    for connection in connections_entities
                ]
                return connections_models
            except Exception as exception:
                database.session.rollback()
                raise exception
