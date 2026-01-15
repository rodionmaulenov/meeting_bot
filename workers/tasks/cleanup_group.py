"""Задача очистки группы в воскресенье."""
import logging
import json

from taskiq import Context, TaskiqDepends

from workers.broker import broker
from repositories.member_repository import MemberRepository
from repositories.invite_link_repository import InviteLinkRepository
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
APPLICATION_MESSAGE_REDIS_KEY = "meeting_bot:application_message"


@broker.task(
    schedule=[{
        "cron": "59 23 * * 0",  # Воскресенье 23:59 Ташкент
        "cron_offset": "Asia/Tashkent"
    }]
)
async def cleanup_group(context: Context = TaskiqDepends()) -> dict:
    """Удалить всех участниц из группы и очистить неиспользованные ссылки."""

    result = {
        "members_kicked": 0,
        "links_deleted": 0,
        "application_message_deleted": False
    }

    # 1. Kick участниц из группы
    member_repository = MemberRepository(supabase=context.state.supabase)
    members = await member_repository.get_all()

    for member in members:
        try:
            await context.state.bot.ban_chat_member(
                chat_id=settings.meeting_group_id,
                user_id=member.telegram_id
            )
            await context.state.bot.unban_chat_member(
                chat_id=settings.meeting_group_id,
                user_id=member.telegram_id
            )
            result["members_kicked"] += 1
            logger.debug(f"Kicked {member.first_name} ({member.telegram_id})")
        except Exception as e:
            logger.error(f"Failed to kick {member.telegram_id}: {e}")

    # 2. Удалить неиспользованные ссылки из БД
    invite_link_repository = InviteLinkRepository(supabase=context.state.supabase)
    result["links_deleted"] = await invite_link_repository.delete_unused()

    # 3. Удалить сообщение с кнопкой анкеты
    application_data = await context.state.redis.get(APPLICATION_MESSAGE_REDIS_KEY)
    if application_data:
        try:
            data = json.loads(application_data)
            await context.state.bot.delete_message(
                chat_id=settings.meeting_group_id,
                message_id=data["message_id"]
            )
            await context.state.redis.delete(APPLICATION_MESSAGE_REDIS_KEY)
            result["application_message_deleted"] = True
            logger.debug(f"Deleted application button message: {data['message_id']}")
        except Exception as e:
            logger.error(f"Failed to delete application message: {e}")

    logger.debug(
        f"Cleanup completed: {result['members_kicked']} kicked, "
        f"{result['links_deleted']} unused links deleted"
    )

    return result