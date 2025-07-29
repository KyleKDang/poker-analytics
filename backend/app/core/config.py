import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # App settings
    APP_NAME: str = "Poker Analytics API"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings() 