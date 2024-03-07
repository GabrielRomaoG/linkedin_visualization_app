from typing import List, Optional
from src.domain.models.shares import Share as ShareModel
from abc import ABC, abstractmethod


class ISharesRepository(ABC):
    """Repository of the shares table"""

    @abstractmethod
    def get_all(self) -> Optional[List[ShareModel]]:
        pass

    """
    Get all records from the shares table

    return:
    List[ShareModel]
    """

    def bulk_insert_shares(self, share_models: List[ShareModel]) -> None:
        pass

    """
    Inserts multiple shares into the database

    args:
    connections_models: List[ShareModel]
    """
