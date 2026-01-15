from datetime import datetime, date

from pydantic import BaseModel


class VideoChatAttendance(BaseModel):
    id: int
    member_id: int
    meeting_date: date
    joined_at: datetime
    left_at: datetime | None
    created_at: datetime