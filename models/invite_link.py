from datetime import datetime
from pydantic import BaseModel


class InviteLink(BaseModel):
    id: int
    link: str
    manager_id: int
    member_name: str
    created_at: datetime
    is_used: bool
