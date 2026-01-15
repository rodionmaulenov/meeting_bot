from supabase import AsyncClient

from models.manager import Manager


class ManagerRepository:
    """Repository для работы с таблицей public.managers"""

    TABLE_NAME = "managers"

    def __init__(self, supabase: AsyncClient):
        self.supabase = supabase

    async def get_by_telegram_id(self, telegram_id: int) -> Manager | None:
        """Найти менеджера по telegram_id"""
        response = await self.supabase.table(self.TABLE_NAME).select("*").eq(
            "telegram_id", telegram_id
        ).execute()

        if not response.data:
            return None

        return Manager(**response.data[0])