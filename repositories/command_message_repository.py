from supabase import AsyncClient
from models.command_message import CommandMessage


class CommandMessageRepository:
    """Repository для работы с таблицей public.commands_messages"""

    TABLE_NAME = "commands_messages"

    def __init__(self, supabase: AsyncClient, bot_type: str):
        self.supabase = supabase
        self.bot_type = bot_type

    async def add_new_message(self, message_id: int) -> None:
        """Сохранить message_id в базу"""
        await self.supabase.table(self.TABLE_NAME).insert({
            "message_id": message_id,
            "bot_type": self.bot_type
        }).execute()

    async def get_all_messages(self) -> list[CommandMessage]:
        """Получить все сообщения для этого бота"""
        response = await self.supabase.table(self.TABLE_NAME).select("*").eq("bot_type", self.bot_type).execute()
        return [CommandMessage(**row) for row in response.data]

    async def delete_all_messages(self) -> None:
        """Удалить все сообщения для этого бота"""
        await self.supabase.table(self.TABLE_NAME).delete().eq("bot_type", self.bot_type).execute()