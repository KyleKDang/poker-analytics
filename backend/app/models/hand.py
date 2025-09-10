from datetime import datetime, timezone
from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ARRAY
from sqlmodel import SQLModel, Column, Field, Relationship

if TYPE_CHECKING:
    from .session import Session


class Position(str, Enum):
    early = "early"
    middle = "middle"
    late = "late"


class Action(str, Enum):
    fold = "fold"
    call = "call"
    raise_ = "raise"


class Result(str, Enum):
    win = "win"
    loss = "loss"
    tie = "tie"


class Hand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")

    hole_cards: list[str] = Field(sa_column=Column(ARRAY(String)), default_factory=list)
    board_cards: list[str] = Field(
        sa_column=Column(ARRAY(String)), default_factory=list
    )

    position: Position
    action_taken: Optional[Action] = None
    result: Optional[Result] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    session: Optional["Session"] = Relationship(back_populates="hands")
