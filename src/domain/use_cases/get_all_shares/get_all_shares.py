from typing import List
import pandas as pd
from src.domain.models.shares import Share
from src.domain.use_cases.get_all_shares.iget_all_shares import IAllSharesGetter
from src.infra.db.repositories.shares.shares_repository import SharesRepository


class AllSharesGetter(IAllSharesGetter):
    def __init__(self, shares_repository=SharesRepository) -> pd.DataFrame:
        self.__shares_repository = shares_repository

    def get_all(self):
        raw_shares = self.__shares_repository().get_all()
        shares_df = self.__shares_list_to_data_frame(raw_shares)
        return shares_df

    @staticmethod
    def __shares_list_to_data_frame(shares_list: List[Share]):
        data_list = [
            {
                "share_link": record.share_link,
                "shared_date": record.shared_date,
                "num_of_comments": record.num_of_comments,
                "num_of_reactions": record.num_of_reactions,
            }
            for record in shares_list
        ]
        shares_df = pd.DataFrame(data_list).astype(
            {
                "shared_date": "datetime64[ns]",
            }
        )
        return shares_df
