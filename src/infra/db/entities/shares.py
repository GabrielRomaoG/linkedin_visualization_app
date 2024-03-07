from datetime import date
from dataclasses import dataclass
from sqlalchemy import String, Date, INTEGER
from sqlalchemy.orm import mapped_column, Mapped
from src.infra.db.settings.base import Base


@dataclass
class Share(Base):
    __tablename__ = "shares"

    share_id: Mapped[str] = mapped_column(String(21), primary_key=True)
    shared_date: Mapped[date | None] = mapped_column(Date)
    num_of_comments: Mapped[int | None] = mapped_column(INTEGER)
    num_of_likes: Mapped[int | None] = mapped_column(INTEGER)
