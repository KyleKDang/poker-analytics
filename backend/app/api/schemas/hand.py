from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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


class HandCreate(BaseModel):
    session_id: int
    hole_cards: list[str] = []
    board_cards: list[str] = []
    position: str
    action_taken: Optional[str] = None
    result: Optional[str] = None


class HandRead(BaseModel):
    id: int
    session_id: int
    hole_cards: list[str]
    board_cards: list[str]
    position: str
    action_taken: Optional[str] = None
    result: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class HandUpdate(BaseModel):
    action_taken: Optional[str] = None
    result: Optional[str] = None
