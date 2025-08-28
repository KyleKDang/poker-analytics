from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .session import Session


class Hand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")

    hole_cards: list[str] = Field(sa_column_kwargs={"type_": "text[]"})
    board_cards: list[str] = Field(sa_column_kwargs={"type_": "text[]"})

    result: str
    position: str
    action_taken: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    session: Optional[Session] = Relationship(back_populates="hands")