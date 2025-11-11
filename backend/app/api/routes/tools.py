from fastapi import APIRouter

from app.api.schemas.hand import (
    HandEvaluationRequest,
    HandEvaluationResponse,
    HandOddsRequest,
    HandOddsResponse,
)
from app.core.evaluator.evaluator import evaluate_hand as evaluate_hand_core
from app.core.odds.odds_calculator import calculate_odds as calculate_odds_core
from app.core.models.card import Card


router = APIRouter(prefix="/tools", tags=["tools"])


def _parse_cards(cards: list[str]) -> list[Card]:
    """Convert a list of string representations into Card objects."""
    return [Card(c) for c in cards]


@router.post("/evaluate", response_model=HandEvaluationResponse)
async def evaluate_hand(request: HandEvaluationRequest):
    """
    Evaluate the best 5-card poker hand from the player's hole cards and board cards.
    """
    all_cards = _parse_cards(request.hole_cards) + _parse_cards(request.board_cards)
    result = evaluate_hand_core(all_cards)
    return HandEvaluationResponse(hand=result["label"], rank=result["rank"])


@router.post("/odds", response_model=HandOddsResponse)
async def calculate_odds(request: HandOddsRequest):
    """
    Calculate winning odds for the given hole cards and board state.
    """
    hole_cards = _parse_cards(request.hole_cards)
    board_cards = _parse_cards(request.board_cards)
    odds = calculate_odds_core(hole_cards, board_cards, request.num_opponents)
    return HandOddsResponse(win=odds["win"], tie=odds["tie"], loss=odds["loss"])
