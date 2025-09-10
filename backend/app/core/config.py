import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Application and database configuration."""

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # App settings
    APP_NAME: str = "Poker Analytics API"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Security / JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


settings = Settings()
