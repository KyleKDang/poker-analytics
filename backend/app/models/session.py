from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .user import User
from .hand import Hand


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

    user: Optional[User] = Relationship(back_populates="sessions")
    hands: list["Hand"] = Relationship(back_populates="session")