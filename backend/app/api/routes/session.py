from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, func, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.schemas.session import SessionCreate, SessionRead
from app.api.schemas.hand import HandRead
from app.models.session import Session as PokerSession
from app.models.hand import Hand as PokerHand
from app.models.user import User
from app.db.session import get_db_session
from app.core.deps import get_current_user


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=list[SessionRead])
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve all poker sessions for the current user with hand counts."""
    result = await db.exec(
        select(PokerSession, func.count(PokerHand.id).label("hand_count"))
        .outerjoin(PokerHand, PokerSession.id == PokerHand.session_id)
        .where(PokerSession.user_id == current_user.id)
        .group_by(PokerSession.id)
        .order_by(desc(PokerSession.start_time))
    )
    sessions_with_counts = []

    for session, hand_count in result.all():
        session_dict = session.model_dump()
        session_dict["hand_count"] = hand_count
        sessions_with_counts.append(session_dict)

    return sessions_with_counts


@router.get("/{session_id}", response_model=SessionRead)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve a single poker session by ID."""
    result = await db.exec(
        select(PokerSession).where(
            PokerSession.id == session_id, PokerSession.user_id == current_user.id
        )
    )
    poker_session = result.first()
    if not poker_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poker session not found"
        )
    return poker_session


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_create: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Create a new poker session for the current user."""
    new_session = PokerSession(user_id=current_user.id, notes=session_create.notes)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a poker session and all its associated hands."""
    result = await db.exec(
        select(PokerSession).where(
            PokerSession.id == session_id, PokerSession.user_id == current_user.id
        )
    )
    poker_session = result.first()
    if not poker_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poker session not found"
        )

    hand_result = await db.exec(
        select(PokerHand).where(PokerHand.session_id == session_id)
    )
    for hand in hand_result.all():
        await db.delete(hand)

    await db.delete(poker_session)
    await db.commit()
    return None


@router.get("/{session_id}/hands", response_model=list[HandRead])
async def get_session_hands(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get all hands for a specific session."""
    result = await db.exec(
        select(PokerSession).where(
            PokerSession.id == session_id, PokerSession.user_id == current_user.id
        )
    )
    poker_session = result.first()
    if not poker_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poker session not found"
        )

    hands_result = await db.exec(
        select(PokerHand).where(PokerHand.session_id == session_id)
    )
    return hands_result.all()
