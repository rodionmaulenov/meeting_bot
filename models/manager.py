from pydantic import BaseModel
from datetime import datetime


class Manager(BaseModel):
    id: int
    telegram_id: int
    name: str
    is_active: bool
    created_at: datetime