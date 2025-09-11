from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.schemas.hand import (
    HandEvaluationRequest,
    HandEvaluationResponse,
    HandOddsRequest,
    HandOddsResponse,
    HandCreate,
    HandRead,
    HandUpdate,
)
from app.db.session import get_db_session
from app.core.evaluator.evaluator import evaluate_seven_card_hand
from app.core.odds.odds_calculator import calculate_odds as calculate_odds_core
from app.core.models.card import Card
from app.models.hand import Hand as PokerHand


router = APIRouter(prefix="/hands", tags=["hands"])


def _parse_cards(cards: list[str]) -> list[Card]:
    """Convert a list of string representations into Card objects."""
    return [Card(c) for c in cards]


@router.get("/{hand_id}", response_model=HandRead)
async def get_hand(hand_id: int, db: AsyncSession = Depends(get_db_session)):
    """Retrieve a single hand by ID."""
    hand = await db.get(PokerHand, hand_id)
    if not hand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hand not found"
        )
    return hand


@router.post("/", response_model=HandRead, status_code=status.HTTP_201_CREATED)
async def create_hand(
    hand_create: HandCreate, db: AsyncSession = Depends(get_db_session)
):
    """Create a new hand for a session."""
    new_hand = PokerHand(**hand_create.model_dump())
    db.add(new_hand)
    await db.commit()
    await db.refresh(new_hand)
    return new_hand


@router.put("/{hand_id}", response_model=HandRead)
async def update_hand(
    hand_id: int, hand_update: HandUpdate, db: AsyncSession = Depends(get_db_session)
):
    """Update a hand's action_taken or result."""
    hand = await db.get(PokerHand, hand_id)
    if not hand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hand not found"
        )

    update_data = hand_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(hand, key, value)

    await db.commit()
    await db.refresh(hand)
    return hand


@router.post("/evaluation", response_model=HandEvaluationResponse)
async def evaluate_hand(request: HandEvaluationRequest):
    """
    Evaluate the best 5-card poker hand from the player's hole cards and board cards.
    """
    all_cards = _parse_cards(request.hole_cards) + _parse_cards(request.board_cards)
    result = evaluate_seven_card_hand(all_cards)
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
