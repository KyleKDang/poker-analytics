from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.session import Session
from app.db.session import get_session
