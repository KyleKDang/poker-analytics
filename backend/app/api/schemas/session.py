from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class SessionCreate(SQLModel):
    user_id: int
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class SessionRead(SQLModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True
