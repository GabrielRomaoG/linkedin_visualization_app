from typing import List, Optional
from src.domain.models.connection import Connection as ConnectionModel
from abc import ABC, abstractmethod


class IConnectionsRepository(ABC):
    """Repository of the connections table"""

    @abstractmethod
    def insert_connection(self, connections_model: ConnectionModel) -> None:
        pass
        """
        Saves record into the connections table

        args:
        connections_model (ConnectionModel)
        """

    @abstractmethod
    def get_all(self) -> Optional[List[ConnectionModel]]:
        pass
        """
        Get all records from the connections table

        return:
        List[ConnectionModel]
        """

    def bulk_insert_connections(
        self, connections_models: List[ConnectionModel]
    ) -> None:
        pass

    """
    Inserts multiple connections into the database

    args:
    connections_models: List[ConnectionsModel]
    """
