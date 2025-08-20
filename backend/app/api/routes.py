from fastapi import APIRouter
from typing import List
from .schema import EvaluateHandRequest
from app.core.evaluator.evaluator import evaluate_seven_card_hand
from app.core.odds.odds_calculator import calculate_odds
from app.core.models.card import Card


router = APIRouter()


@router.post("/evaluate-hand")
def evaluate_hand(request: EvaluateHandRequest):
    hole_cards = [Card(c) for c in request.hole_cards]
    board_cards = [Card(c) for c in request.board_cards]
    all_cards = hole_cards + board_cards
    result = evaluate_seven_card_hand(all_cards)
    return {
        "hand": result["label"],
        "rank": result["rank"]
    }