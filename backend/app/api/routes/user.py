from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.api.schemas.user import UserRead


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)
):
    """Retrieve a list of registered users."""
    result = await db.exec(select(User).offset(skip).limit(limit))
    return result.all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    """Retrieve a single user by ID."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user