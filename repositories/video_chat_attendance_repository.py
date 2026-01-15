import logging
from datetime import date, datetime

from supabase import AsyncClient

from models.video_chat_attendance import VideoChatAttendance

logger = logging.getLogger(__name__)


class VideoChatAttendanceRepository:
    TABLE_NAME = "video_chat_attendance"
    SCHEMA = "meeting"

    def __init__(self, supabase: AsyncClient):
        self.supabase = supabase

    async def create(self, member_id: int, meeting_date: date, joined_at: datetime) -> VideoChatAttendance:
        """Создать запись о входе в Video Chat."""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).insert({
            "member_id": member_id,
            "meeting_date": meeting_date.isoformat(),
            "joined_at": joined_at.isoformat()
        }).execute()

        logger.debug(f"Created attendance record for member_id={member_id}")
        return VideoChatAttendance(**response.data[0])

    async def update_left_at(self, member_id: int, meeting_date: date, left_at: datetime) -> None:
        """Обновить время выхода из Video Chat."""
        await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).update({
            "left_at": left_at.isoformat()
        }).eq(
            "member_id", member_id
        ).eq(
            "meeting_date", meeting_date.isoformat()
        ).is_(
            "left_at", "null"
        ).execute()

        logger.debug(f"Updated left_at for member_id={member_id}")
