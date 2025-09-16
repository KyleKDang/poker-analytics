from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.routes import hand, session, user, auth
from app.db.session import create_db_and_tables, get_db_session
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(hand.router)
app.include_router(session.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Hello, Poker Analytics!"}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    try:
        await db.exec(select(1))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "healthy", "database": db_status}
