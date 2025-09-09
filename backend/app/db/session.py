from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings


# Async engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# Dependency for FastAPI routes
async def get_db_session():
    async with async_session() as session:
        yield session


# Create all tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
