"""Репозиторий для статистики."""
from datetime import datetime

from postgrest import CountMethod
from supabase import AsyncClient


class StatisticsRepository:
    """Репозиторий для получения данных статистики."""

    def __init__(self, supabase: AsyncClient):
        self.supabase = supabase

    async def get_active_managers(self) -> list[dict]:
        """Получить всех активных менеджеров."""
        response = await self.supabase.table("managers").select(
            "id, name"
        ).eq("is_active", True).execute()

        return response.data

    async def get_members_by_manager(
        self,
        manager_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> list[dict]:
        """Получить участниц менеджера за период."""
        response = await self.supabase.schema("meeting").table(
            "members"
        ).select(
            "id, joined_at, invite_links!inner(manager_id)"
        ).eq(
            "invite_links.manager_id", manager_id
        ).gte(
            "joined_at", start_date.isoformat()
        ).lte(
            "joined_at", end_date.isoformat()
        ).execute()

        return response.data

    async def get_video_attendance_by_members(
        self,
        member_ids: list[int],
        start_date: datetime,
        end_date: datetime
    ) -> list[dict]:
        """Получить посещения видеочата для участниц."""
        if not member_ids:
            return []

        response = await self.supabase.schema("meeting").table(
            "video_chat_attendance"
        ).select(
            "member_id, joined_at, left_at"
        ).in_(
            "member_id", member_ids
        ).gte(
            "meeting_date", start_date.date().isoformat()
        ).lte(
            "meeting_date", end_date.date().isoformat()
        ).execute()

        return response.data

    async def get_applications_count_by_status(
        self,
        manager_id: int,
        status: str,
        start_date: datetime,
        end_date: datetime
    ) -> int:
        """Получить количество анкет по статусу."""
        response = await self.supabase.schema("meeting").table(
            "applications"
        ).select(
            "id", count=CountMethod.exact
        ).eq(
            "manager_id", manager_id
        ).eq(
            "status", status
        ).gte(
            "created_at", start_date.isoformat()
        ).lte(
            "created_at", end_date.isoformat()
        ).execute()

        return response.count or 0