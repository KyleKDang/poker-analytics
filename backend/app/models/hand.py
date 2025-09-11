from datetime import datetime
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

    player_position: Position = Field(sa_column=(Column(String, nullable=False)))
    action_taken: Optional[Action] = Field(sa_column=Column(String), default=None)
    result: Optional[Result] = Field(sa_column=Column(String), default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    session: Optional["Session"] = Relationship(back_populates="hands")
