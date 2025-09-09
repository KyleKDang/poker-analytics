from pydantic import BaseModel


class EvaluateHandRequest(BaseModel):
    hole_cards: list[str]
    board_cards: list[str]


class CalculateOddsRequest(BaseModel):
    hole_cards: list[str]
    board_cards: list[str]
    num_opponents: int
