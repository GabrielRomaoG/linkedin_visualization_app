from typing import List
from src.domain.models.connection import Connection as ConnectionModel
from abc import ABC, abstractmethod


class IConnectionsRepository(ABC):
    """Repository of the connections table"""

    @abstractmethod
    def insert_connection(self, connections_model: ConnectionModel) -> None:
        """
        Saves record into the connections table

        args:
        connections_model (ConnectionModel)
        """

    @abstractmethod
    def get_all(self) -> List[ConnectionModel]:
        """
        Get all records from the connections table

        return:
        List[ConnectionModel]
        """
