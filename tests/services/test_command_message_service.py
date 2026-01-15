from unittest.mock import AsyncMock

import pytest
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from services.command_message_service import CommandMessageService
from models.command_message import CommandMessage


class TestCommandMessageService:

    @pytest.fixture
    def mock_bot(self) -> AsyncMock:
        """Mock для Telegram Bot"""
        return AsyncMock(spec=Bot)

    @pytest.fixture
    def mock_repository(self) -> AsyncMock:
        """Mock для CommandMessageRepository"""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_bot, mock_repository) -> CommandMessageService:
        """Создать service с mock зависимостями"""
        return CommandMessageService(
            bot=mock_bot,
            repository=mock_repository,
            chat_id=-1001234567890
        )

    async def test_clear_messages_deletes_all_messages_from_telegram(
            self,
            service: CommandMessageService,
            mock_bot: AsyncMock,
            mock_repository: AsyncMock
    ):
        """Тест: clear_messages удаляет все сообщения из Telegram"""
        # Arrange
        mock_repository.get_all_messages.return_value = [
            CommandMessage(id=1, message_id=111, bot_type="test", created_at="2025-01-01T00:00:00"),
            CommandMessage(id=2, message_id=222, bot_type="test", created_at="2025-01-01T00:00:00"),
        ]

        # Act
        deleted_count = await service.clear_messages()

        # Assert
        assert deleted_count == 2
        assert mock_bot.delete_message.call_count == 2
        mock_repository.delete_all_messages.assert_called_once()

    async def test_clear_messages_returns_zero_when_no_messages(
            self,
            service: CommandMessageService,
            mock_repository: AsyncMock
    ):
        """Тест: clear_messages возвращает 0 если нет сообщений"""
        mock_repository.get_all_messages.return_value = []

        deleted_count = await service.clear_messages()

        assert deleted_count == 0

    async def test_clear_messages_handles_telegram_error(
            self,
            service: CommandMessageService,
            mock_bot: AsyncMock,
            mock_repository: AsyncMock
    ):
        """Тест: clear_messages обрабатывает ошибку если сообщение не найдено"""
        mock_repository.get_all_messages.return_value = [
            CommandMessage(id=1, message_id=111, bot_type="test", created_at="2025-01-01T00:00:00"),
            CommandMessage(id=2, message_id=222, bot_type="test", created_at="2025-01-01T00:00:00"),
        ]

        # Первое сообщение удалится, второе вызовет ошибку
        mock_bot.delete_message.side_effect = [
            None,
            TelegramBadRequest(method="deleteMessage", message="message not found")
        ]

        deleted_count = await service.clear_messages()

        assert deleted_count == 1  # только одно удалилось
        mock_repository.delete_all_messages.assert_called_once()  # cleanup всё равно вызван