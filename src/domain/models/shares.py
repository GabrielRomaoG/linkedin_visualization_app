from datetime import date
from dataclasses import dataclass


@dataclass
class Share:
    share_id: str
    shared_date: date | None = None
    num_of_comments: int | None = None
    num_of_likes: int | None = None
