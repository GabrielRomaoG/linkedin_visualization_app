from abc import ABC, abstractmethod
import pandas as pd


class IAllConnectionsGetter(ABC):
    """Interface for retrieving all connections as a DataFrame."""

    @abstractmethod
    def get_all(self) -> pd.DataFrame:
        """Retrieves all connections as a pandas DataFrame.

        Returns:
            A DataFrame containing the retrieved connections.
        """
