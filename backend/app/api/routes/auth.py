from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.api.schemas.user import UserRegister, UserLogin, UserRead, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserRegister, db: AsyncSession = Depends(get_db_session)
):
    """Register a new user."""
    result = await db.exec(
        select(User).where(
            (User.username == user_create.username) | (User.email == user_create.email)
        )
    )
    existing_user = result.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserRead.model_validate(new_user)


@router.post("/login", response_model=TokenResponse)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db_session)):
    """Authenticate a user and return a JWT access token."""
    result = await db.exec(select(User).where(User.username == user_login.username))
    user = result.first()
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)
