from datetime import date
from dataclasses import dataclass


@dataclass
class Share:
    share_link: str
    shared_date: date | None = None
    num_of_comments: int | None = None
    num_of_reactions: int | None = None
