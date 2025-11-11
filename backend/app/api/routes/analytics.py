from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.schemas.hand import (
    HandEvaluationRequest,
    HandEvaluationResponse,
    HandOddsRequest,
    HandOddsResponse,
)
from app.db.session import get_db_session
from app.core.deps import get_current_user
from app.core.evaluator.evaluator import evaluate_hand as evaluate_hand_core
from app.core.odds.odds_calculator import calculate_odds as calculate_odds_core
from app.core.models.card import Card
from app.models.user import User
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["analytics"])


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


@router.get("/overview")
async def get_analytics_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get overall analytics overview for the current user."""
    overall_stats = await AnalyticsService.get_overall_stats(db, current_user.id)
    return overall_stats


@router.get("/position")
async def get_position_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get analytics by position."""
    position_stats = await AnalyticsService.get_position_stats(db, current_user.id)
    return position_stats


@router.get("/action")
async def get_action_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get analytics by action."""
    action_stats = await AnalyticsService.get_action_stats(db, current_user.id)
    return action_stats


@router.get("/timeline")
async def get_timeline_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get win rate over time."""
    timeline = await AnalyticsService.get_win_rate_over_time(db, current_user.id)
    return timeline


@router.get("/sessions")
async def get_session_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get session performance analytics."""
    sessions = await AnalyticsService.get_session_performance(db, current_user.id)
    return sessions


@router.get("/heatmap")
async def get_position_heatmap(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get position heat map data."""
    heatmap = await AnalyticsService.get_position_heatmap(db, current_user.id)
    return heatmap


@router.get("/style")
async def get_playing_style(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get playing style profile."""
    style = await AnalyticsService.get_playing_style_profile(db, current_user.id)
    return style


@router.get("/dashboard")
async def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get all dashboard data in a single request."""
    overall_stats = await AnalyticsService.get_overall_stats(db, current_user.id)
    position_stats = await AnalyticsService.get_position_stats(db, current_user.id)
    action_stats = await AnalyticsService.get_action_stats(db, current_user.id)
    timeline = await AnalyticsService.get_win_rate_over_time(db, current_user.id)
    style = await AnalyticsService.get_playing_style_profile(db, current_user.id)

    return {
        "overall": overall_stats,
        "positions": position_stats,
        "actions": action_stats,
        "timeline": timeline,
        "style": style,
    }
