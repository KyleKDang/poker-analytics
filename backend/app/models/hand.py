from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .session import Session

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import SQLModel, Field, Relationship


class Hand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")

    hole_cards: list[str] = Field(
        sa_column=Column(ARRAY(String)), 
        default_factory=list
    )
    board_cards: list[str] = Field(
        sa_column=Column(ARRAY(String)), 
        default_factory=list
    )

    result: str
    position: str
    action_taken: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    session: Optional["Session"] = Relationship(back_populates="hands")