from datetime import date, datetime


class Connection:
    user_name: str
    company: str | None
    position: str | None
    connected_on: datetime | None

    def __init__(
        self,
        user_name: str | None,
        company: str | None,
        position: str | None,
        connected_on: date,
    ):
        self.user_name = user_name
        self.company = company
        self.position = position
        self.connected_on = connected_on
