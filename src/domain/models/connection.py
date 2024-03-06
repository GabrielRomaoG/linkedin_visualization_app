from datetime import date
from dataclasses import dataclass


@dataclass
class Connection:
    user_name: str
    company: str | None = None
    position: str | None = None
    connected_on: date | None = None
