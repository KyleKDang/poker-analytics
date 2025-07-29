from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Create all tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Get database session
def get_session():
    with Session(engine) as session:
        yield session 