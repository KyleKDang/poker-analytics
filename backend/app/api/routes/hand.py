from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.schemas.hand import (
    HandCreate,
    HandRead,
    HandUpdate,
)
from app.db.session import get_db_session
from app.models.hand import Hand as PokerHand


router = APIRouter(prefix="/hands", tags=["hands"])


@router.get("/{hand_id}", response_model=HandRead)
async def get_hand(hand_id: int, db: AsyncSession = Depends(get_db_session)):
    """Retrieve a single hand by ID."""
    hand = await db.get(PokerHand, hand_id)
    if not hand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hand not found"
        )
    return hand


@router.post("", response_model=HandRead, status_code=status.HTTP_201_CREATED)
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


@router.delete("/{hand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hand(hand_id: int, db: AsyncSession = Depends(get_db_session)):
    """Delete a specific hand."""
    hand = await db.get(PokerHand, hand_id)
    if not hand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hand not found"
        )

    await db.delete(hand)
    await db.commit()
    return None
