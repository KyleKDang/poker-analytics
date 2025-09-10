from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class HandEvaluationRequest(BaseModel):
    hole_cards: list[str]
    board_cards: list[str]


class HandEvaluationResponse(BaseModel):
    hand: str
    rank: int


class HandOddsRequest(BaseModel):
    hole_cards: list[str]
    board_cards: list[str]
    num_opponents: int


class HandOddsResponse(BaseModel):
    win: float
    tie: float
    loss: float


class HandBase(SQLModel):
    session_id: int
    hole_cards: list[str] = []
    board_cards: list[str] = []
    position: str
    action_taken: Optional[str] = None
    result: Optional[str] = None


class HandCreate(HandBase):
    pass


class HandRead(HandBase):
    id: int
    created_at: datetime

    class Config:
        form_attributes = True


class HandUpdate(SQLModel):
    action_taken: Optional[str] = None
    result: Optional[str] = None
