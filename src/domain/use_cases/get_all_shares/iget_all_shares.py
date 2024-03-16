from abc import ABC, abstractmethod
import pandas as pd


class IAllSharesGetter(ABC):
    """Interface for retrieving all shares as a DataFrame."""

    @abstractmethod
    def get_all(self) -> pd.DataFrame:
        """Retrieves all shares as a pandas DataFrame.

        Returns:
            A DataFrame containing the retrieved shares.
        """
