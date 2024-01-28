from datetime import date
from dataclasses import dataclass
from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from src.infra.db.settings.base import Base


@dataclass
class Connection(Base):
    __tablename__ = "connections"

    user_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    company: Mapped[str | None] = mapped_column(String(255))
    position: Mapped[str | None] = mapped_column(String(255))
    connected_on: Mapped[date | None] = mapped_column(Date)
