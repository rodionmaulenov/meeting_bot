from pydantic import BaseModel
from datetime import datetime

class CommandMessage(BaseModel):
    id: int
    message_id: int
    bot_type: str
    created_at: datetime