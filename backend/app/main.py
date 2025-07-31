from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.db.session import create_db_and_tables, get_session
from app.models.user import User
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, Poker Analytics!"}


@app.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        session.exec(select(User).limit(1)).first()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "healthy", "database": db_status}


@app.get("/users")
def get_users(
    session: Session = Depends(get_session), 
    skip: int = 0, 
    limit: int = 10
):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users