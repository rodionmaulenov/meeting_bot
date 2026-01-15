from supabase import AsyncClient

from models.invite_link import InviteLink


class InviteLinkRepository:
    """Repository для работы с таблицей meeting.invite_links"""

    TABLE_NAME = "invite_links"
    SCHEMA = "meeting"

    def __init__(self, supabase: AsyncClient):
        self.supabase = supabase

    async def create(self, link: str, manager_id: int, member_name: str) -> InviteLink:
        """Создать новую invite-ссылку"""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).insert({
            "link": link,
            "manager_id": manager_id,
            "member_name": member_name,
            "is_used": False
        }).execute()

        return InviteLink(**response.data[0])

    async def get_by_link(self, link: str) -> InviteLink | None:
        """Найти ссылку по URL (когда кто-то переходит)"""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).select("*").eq("link", link).execute()

        if not response.data:
            return None

        return InviteLink(**response.data[0])

    async def get_by_id(self, link_id: int) -> InviteLink | None:
        """Найти ссылку по ID."""
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).select(
            "*"
        ).eq("id", link_id).execute()

        if not response.data:
            return None

        return InviteLink(**response.data[0])

    async def mark_as_used(self, link_id: int) -> None:
        """Пометить ссылку как использованную"""
        await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).update({
            "is_used": True
        }).eq("id", link_id).execute()

    async def delete_unused(self) -> int:
        """Удалить все неиспользованные ссылки.

        Returns:
            Количество удалённых ссылок
        """
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).delete().eq(
            "is_used", False
        ).execute()

        return len(response.data)