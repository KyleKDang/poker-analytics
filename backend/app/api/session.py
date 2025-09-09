from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.session import Session as PokerSession
from app.db.session import get_db_session
from .schemas.session import SessionCreate, SessionRead


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/", response_model=list[SessionRead])
async def get_sessions(db: AsyncSession = Depends(get_db_session)):
    """Retrieve all poker sessions."""
    result = await db.exec(select(PokerSession))
    return result.all()


@router.get("/{session_id}", response_model=SessionRead)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db_session)):
    """Retrieve a single poker session by ID."""
    result = await db.exec(select(PokerSession).where(PokerSession.id == session_id))
    poker_session = result.first()
    if not poker_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poker session not found"
        )
    return poker_session


@router.post("/", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_create: SessionCreate, db: AsyncSession = Depends(get_db_session)
):
    """Create a new poker session."""
    new_session = PokerSession(**session_create.model_dump())
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session
