import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from config import get_settings
from repositories.command_message_repository import CommandMessageRepository
from repositories.manager_repository import ManagerRepository
from templates import RestrictionTemplate

settings = get_settings()
logger = logging.getLogger(__name__)


class CommandsMiddleware(BaseMiddleware):
    """Middleware для команд: проверка прав + сохранение сообщений."""

    def __init__(
            self,
            manager_repository: ManagerRepository,
            command_message_repository: CommandMessageRepository
    ):
        self.manager_repository = manager_repository
        self.command_message_repository = command_message_repository

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any | None:

        # Пропускаем если не тот тред
        if event.message_thread_id != settings.commands_thread_id:
            return await handler(event, data)

        # Сохраняем входящее сообщение
        logger.debug(f"Saving incoming message_id={event.message_id}")
        await self.command_message_repository.add_new_message(event.message_id)

        # Проверяем права ПЕРЕД вызовом handler
        manager = await self.manager_repository.get_by_telegram_id(event.from_user.id)

        if manager is None:
            logger.warning(f"Access denied for user_id={event.from_user.id}")
            response = await event.answer(RestrictionTemplate.you_are_not_manager())
            if response:
                await self.command_message_repository.add_new_message(response.message_id)
            return None

        # Вызываем handler только если есть права
        result = await handler(event, data)

        # Сохраняем ответ бота
        if result and hasattr(result, 'message_id'):
            logger.debug(f"Saving bot response message_id={result.message_id}")
            await self.command_message_repository.add_new_message(result.message_id)

        return result