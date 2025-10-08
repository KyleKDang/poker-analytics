from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionCreate(BaseModel):
    notes: Optional[str] = None


class SessionRead(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    notes: Optional[str] = None
    hand_count: int = 0

    model_config = {"from_attributes": True}
