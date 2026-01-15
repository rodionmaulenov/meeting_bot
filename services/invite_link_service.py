import logging
from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.types import ChatInviteLink

from repositories.invite_link_repository import InviteLinkRepository
from models.invite_link import InviteLink
from repositories.manager_repository import ManagerRepository
from utils.formatters import shorten_name

logger = logging.getLogger(__name__)


class InviteLinkService:
    """Сервис для работы с invite-ссылками"""

    LINK_EXPIRE_HOURS = 24

    def __init__(
            self,
            bot: Bot,
            manager_repository: ManagerRepository,
            invite_link_repository: InviteLinkRepository,
            group_id: int
    ):
        self.bot = bot
        self.manager_repository = manager_repository
        self.invite_link_repository = invite_link_repository
        self.group_id = group_id

    async def create_invite_link(self, manager_telegram_id: int, member_name: str) -> InviteLink:
        """Создать invite-ссылку для новой участницы"""

        # 1. Проверяем что менеджер существует
        manager = await self.manager_repository.get_by_telegram_id(manager_telegram_id)
        if not manager:
            raise ValueError("Manager not found")

        # 2. Создаём ссылку в Telegram
        now = datetime.now(timezone.utc)
        expire_date = now + timedelta(hours=self.LINK_EXPIRE_HOURS)
        telegram_link: ChatInviteLink = await self.bot.create_chat_invite_link(
            chat_id=self.group_id,
            expire_date=expire_date,
            member_limit=1,
            name=shorten_name(member_name)
        )

        logger.debug(f"Created Telegram invite link for '{member_name}': {telegram_link.invite_link}")

        # 3. Сохраняем в базу данных
        invite_link = await self.invite_link_repository.create(
            link=telegram_link.invite_link,
            manager_id=manager.id,
            member_name=member_name
        )

        logger.debug(f"Saved invite link to database: id={invite_link.id}")

        return invite_link

    async def get_link_by_url(self, url: str) -> InviteLink | None:
        """Найти ссылку по URL"""
        return await self.invite_link_repository.get_by_link(url)

    async def mark_link_as_used(self, link_id: int) -> None:
        """Пометить ссылку как использованную"""
        await self.invite_link_repository.mark_as_used(link_id)
        logger.debug(f"Marked invite link {link_id} as used")
