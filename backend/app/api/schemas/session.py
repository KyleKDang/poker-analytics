from sqlmodel import SQLModel
from typing import Optional


class SessionCreate(SQLModel):
    user_id: int
    notes: Optional[str] = None
    end_time: Optional[str] = None

    class Config:
        orm_mode = True


class SessionRead(SQLModel):
    id: int
    user_id: int
    notes: Optional[str] = None
    end_time: Optional[str] = None

    class Config:
        orm_mode = True
