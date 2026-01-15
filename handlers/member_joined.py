"""Handler для входа участниц в Meeting Group."""
import logging
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated

from config import get_settings
from repositories.member_repository import MemberRepository
from services.invite_link_service import InviteLinkService

logger = logging.getLogger(__name__)
router = Router()
settings = get_settings()


@router.chat_member(
    F.chat.id == settings.meeting_group_id,
    F.new_chat_member.status == "member",
    F.invite_link,
)
async def on_member_joined(
        event: ChatMemberUpdated,
        invite_link_service: InviteLinkService,
        member_repository: MemberRepository
) -> None:
    """Девушка вошла в группу по invite-ссылке."""

    user = event.new_chat_member.user
    link_url = event.invite_link.invite_link

    # 1. Найти ссылку в БД
    invite_link = await invite_link_service.get_link_by_url(link_url)
    if not invite_link:
        logger.warning(f"Unknown invite link: {link_url}")
        return

    # 2. Пометить как использованную
    await invite_link_service.mark_link_as_used(invite_link.id)

    # 3. Сохранить участницу
    member = await member_repository.create(
        telegram_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        invite_link_id=invite_link.id
    )

    logger.info(f"New member joined: {user.first_name} (id={member.id})")