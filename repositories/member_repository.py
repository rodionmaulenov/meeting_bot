from supabase import AsyncClient

from models.member import Member


class MemberRepository:
    """Repository для работы с таблицей meeting.members"""

    TABLE_NAME = "members"
    SCHEMA = "meeting"

    def __init__(self, supabase: AsyncClient):
        self.supabase = supabase

    async def create(
            self,
            telegram_id: int,
            first_name: str,
            last_name: str | None,
            username: str | None,
            invite_link_id: int
    ) -> Member:
        """Сохранить нового участника"""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).insert({
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "invite_link_id": invite_link_id,
        }).execute()

        return Member(**response.data[0])

    async def get_all(self) -> list[Member]:
        """Получить всех участниц."""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).select("*").execute()
        return [Member(**row) for row in response.data]

    async def get_by_telegram_id(self, telegram_id: int) -> Member | None:
        """Найти участницу по Telegram ID."""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).select(
            "*"
        ).eq("telegram_id", telegram_id).execute()

        if not response.data:
            return None

        return Member(**response.data[0])
