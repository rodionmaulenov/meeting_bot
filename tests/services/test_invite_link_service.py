from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import Bot
from aiogram.types import ChatInviteLink

from models.manager import Manager
from models.invite_link import InviteLink
from repositories.manager_repository import ManagerRepository
from repositories.invite_link_repository import InviteLinkRepository
from services.invite_link_service import InviteLinkService


class TestInviteLinkService:

    @pytest.fixture
    def mock_bot(self) -> AsyncMock:
        bot = AsyncMock(spec=Bot)
        bot.create_chat_invite_link.return_value = MagicMock(
            spec=ChatInviteLink,
            invite_link="https://t.me/+abc123"
        )
        return bot

    @pytest.fixture
    def mock_manager_repository(self) -> AsyncMock:
        return AsyncMock(spec=ManagerRepository)

    @pytest.fixture
    def mock_invite_link_repository(self) -> AsyncMock:
        return AsyncMock(spec=InviteLinkRepository)

    @pytest.fixture
    def service(
            self,
            mock_bot: AsyncMock,
            mock_manager_repository: AsyncMock,
            mock_invite_link_repository: AsyncMock
    ) -> InviteLinkService:
        return InviteLinkService(
            bot=mock_bot,
            manager_repository=mock_manager_repository,
            invite_link_repository=mock_invite_link_repository,
            group_id=-1001234567890
        )

    @pytest.fixture
    def sample_manager(self) -> Manager:
        return Manager(
            id=1,
            telegram_id=123456,
            name="Test Manager",
            is_active=True,
            created_at=datetime.now()
        )

    @pytest.fixture
    def sample_invite_link(self) -> InviteLink:
        return InviteLink(
            id=1,
            link="https://t.me/+abc123",
            manager_id=1,
            member_name="Иванова Анна Петровна",
            is_used=False,
            created_at=datetime.now()
        )

    async def test_create_invite_link_success(
            self,
            service: InviteLinkService,
            mock_manager_repository: AsyncMock,
            mock_invite_link_repository: AsyncMock,
            sample_manager: Manager,
            sample_invite_link: InviteLink
    ):
        mock_manager_repository.get_by_telegram_id.return_value = sample_manager
        mock_invite_link_repository.create.return_value = sample_invite_link

        result = await service.create_invite_link(
            manager_telegram_id=123456,
            member_name="Иванова Анна Петровна"
        )

        assert result == sample_invite_link

    async def test_create_invite_link_raises_when_manager_not_found(
            self,
            service: InviteLinkService,
            mock_manager_repository: AsyncMock
    ):
        mock_manager_repository.get_by_telegram_id.return_value = None

        with pytest.raises(ValueError, match="Manager not found"):
            await service.create_invite_link(
                manager_telegram_id=999999,
                member_name="Test Name"
            )

    async def test_create_invite_link_uses_shortened_name(
            self,
            service: InviteLinkService,
            mock_manager_repository: AsyncMock,
            mock_invite_link_repository: AsyncMock,
            mock_bot: AsyncMock,
            sample_manager: Manager,
            sample_invite_link: InviteLink
    ):
        mock_manager_repository.get_by_telegram_id.return_value = sample_manager
        mock_invite_link_repository.create.return_value = sample_invite_link

        await service.create_invite_link(
            manager_telegram_id=123456,
            member_name="Иванова Анна Петровна"
        )

        call_kwargs = mock_bot.create_chat_invite_link.call_args.kwargs
        assert call_kwargs["name"] == "Иванова А.П."

    async def test_get_link_by_url_returns_invite_link(
            self,
            service: InviteLinkService,
            mock_invite_link_repository: AsyncMock,
            sample_invite_link: InviteLink
    ):
        mock_invite_link_repository.get_by_link.return_value = sample_invite_link

        result = await service.get_link_by_url("https://t.me/+abc123")

        assert result == sample_invite_link