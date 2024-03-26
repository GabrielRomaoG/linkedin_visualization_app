from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from src.domain.models.connection import Connection


class IAllConnectionsGetter(ABC):
    """Interface for retrieving all connections as a DataFrame."""

    @abstractmethod
    def get_all(self) -> pd.DataFrame:
        """Retrieves all connections as a pandas DataFrame.

        Returns:
            A DataFrame containing the retrieved connections.
        """

    @classmethod
    @abstractmethod
    def connections_list_to_data_frame(cls, connections_list: List[Connection]):
        """
        Converts a list of Connection Models into a dataframe

        arg:
            - List[Connection]: Listo of connection models
        """
        pass
