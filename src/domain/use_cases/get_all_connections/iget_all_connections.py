from abc import ABC, abstractmethod


class AllConnectionsGetterInterface(ABC):
    """Interface for retrieving all connections as a DataFrame."""

    @abstractmethod
    def get_all(self):
        """Retrieves all connections as a pandas DataFrame.

        Returns:
            A DataFrame containing the retrieved connections.
        """
