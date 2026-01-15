import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from repositories.command_message_repository import CommandMessageRepository

logger = logging.getLogger(__name__)


class CommandMessageService:

    def __init__(self, bot: Bot, repository: CommandMessageRepository, chat_id: int):
        self.bot = bot
        self.repository = repository
        self.chat_id = chat_id

    async def clear_messages(self) -> int:
        messages = await self.repository.get_all_messages()

        logger.info(f"Found {len(messages)} messages to delete")

        deleted_count = 0
        for message in messages:
            try:
                await self.bot.delete_message(chat_id=self.chat_id, message_id=message.message_id)
                deleted_count += 1
            except TelegramBadRequest as e:
                logger.warning(f"Cannot delete message {message.message_id}: {e}")
            except TelegramForbiddenError as e:
                logger.error(f"No permission to delete message {message.message_id}: {e}")

        await self.repository.delete_all_messages()

        logger.info(f"Deleted {deleted_count} messages")
        return deleted_count