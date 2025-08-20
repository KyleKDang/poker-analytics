from pydantic import BaseModel
from typing import List

class EvaluateHandRequest(BaseModel):
    hole_cards: List[str]
    board_cards: List[str]

class CalculateOddsRequest(BaseModel):
    hole_cards: List[str]
    board_cards: List[str]
    num_opponents: int