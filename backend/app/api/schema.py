from pydantic import BaseModel
from typing import List

class EvaluateHandRequest(BaseModel):
    hole_cards: List[str]
    board_cards: List[str]