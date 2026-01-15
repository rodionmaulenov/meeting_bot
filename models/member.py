from pydantic import BaseModel
from datetime import datetime

class Member(BaseModel):
    id: int
    telegram_id: int
    first_name: str
    last_name: str | None
    username: str | None
    invite_link_id: int  # FK → invite_links.id
    joined_at: datetime