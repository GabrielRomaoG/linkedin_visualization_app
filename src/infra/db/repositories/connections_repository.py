from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.connections import Connection as ConnectionEntity
from src.domain.models.connection import Connection as ConnectionModel


class ConnectionsRepository:
    @classmethod
    def __entity_to_model(cls, entity: ConnectionEntity) -> ConnectionModel:
        return ConnectionModel(
            user_name=entity.user_name,
            company=entity.company,
            position=entity.position,
            connected_on=entity.connected_on,
        )

    @classmethod
    def __model_to_entity(cls, model: ConnectionModel) -> ConnectionEntity:
        return ConnectionEntity(
            user_name=model.user_name,
            company=model.company,
            position=model.position,
            connected_on=model.connected_on,
        )

    def insert_connection(self, connections_model: ConnectionModel) -> None:
        new_registry = self.__model_to_entity(connections_model)
        with DBConnectionHandler() as database:
            try:
                database.session.add(new_registry)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception
