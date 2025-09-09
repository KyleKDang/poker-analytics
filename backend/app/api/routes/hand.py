from fastapi import APIRouter, status

from app.api.schemas.hand import EvaluateHandRequest, CalculateOddsRequest
from app.core.evaluator.evaluator import evaluate_seven_card_hand
from app.core.odds.odds_calculator import calculate_odds as calculate_odds_core
from app.core.models.card import Card


router = APIRouter(prefix="/hands", tags=["hands"])


def _parse_cards(cards: list[str]) -> list[Card]:
    """Convert a list of string representations into Card objects."""
    return [Card(c) for c in cards]


@router.post("/evaluation", status_code=status.HTTP_200_OK)
def evaluate_hand(request: EvaluateHandRequest) -> dict[str, str | int]:
    """
    Evaluate the best 5-card poker hand from the player's hole cards and board cards.

    Returns a dictionary with:
        - hand (str): Human-readable hand label (e.g., "Two Pair").
        - rank (int): Numerical rank of the hand.
    """
    all_cards = _parse_cards(request.hole_cards) + _parse_cards(request.board_cards)
    result = evaluate_seven_card_hand(all_cards)
    return {"hand": result["label"], "rank": result["rank"]}


@router.post("/odds", status_code=status.HTTP_200_OK)
def calculate_odds(request: CalculateOddsRequest) -> dict[str, float]:
    """
    Calculate winning odds for the given hole cards and board state.

    Returns a dictionary with:
        - win (float): Probability of winning.
        - tie (float): Probability of tying.
        - loss (float): Probability of losing.
    """
    hole_cards = _parse_cards(request.hole_cards)
    board_cards = _parse_cards(request.board_cards)
    return calculate_odds_core(hole_cards, board_cards, request.num_opponents)
