from typing import List
import pandas as pd
from src.domain.models.connection import Connection
from src.domain.use_cases.get_all_connections.iget_all_connections import (
    IAllConnectionsGetter,
)
from src.infra.db.repositories.connections.connections_repository import (
    ConnectionsRepository,
)


class AllConnectionsGetter(IAllConnectionsGetter):
    def __init__(self, connections_repository=ConnectionsRepository) -> pd.DataFrame:
        self.__connections_repository = connections_repository

    def get_all(self):
        raw_connections = self.__connections_repository().get_all()
        connections_df = self.connections_list_to_data_frame(raw_connections)
        return connections_df

    @classmethod
    def connections_list_to_data_frame(cls, connections_list: List[Connection]):
        connections_df = pd.DataFrame(connections_list).astype(
            {
                "connected_on": "datetime64[ns]",
            }
        )
        return connections_df
