from pydantic import BaseModel


class EvaluateHandRequest(BaseModel):
    """Request body for evaluating a poker hand."""

    hole_cards: list[str]
    board_cards: list[str]


class CalculateOddsRequest(BaseModel):
    """Request body for calculating poker winning odds."""

    hole_cards: list[str]
    board_cards: list[str]
    num_opponents: int
