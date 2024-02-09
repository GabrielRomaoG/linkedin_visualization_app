from datetime import date


class Connection:
    user_name: str
    company: str | None
    position: str | None
    connected_on: date | None

    def __init__(
        self,
        user_name: str | None,
        company: str | None,
        position: str | None,
        connected_on: date,
    ) -> None:
        self.user_name = user_name
        self.company = company
        self.position = position
        self.connected_on = connected_on

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return NotImplemented
        return (
            self.user_name == other.user_name
            and self.company == other.company
            and self.position == other.position
            and self.connected_on == other.connected_on
        )
