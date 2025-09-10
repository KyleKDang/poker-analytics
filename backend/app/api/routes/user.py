from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db_session
from app.models.user import User
from app.api.schemas.user import UserCreate, UserLogin, UserRead, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token


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
    """Retrieve a single user by their ID."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db_session)):
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
