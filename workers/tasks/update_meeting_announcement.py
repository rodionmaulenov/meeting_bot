"""Задача обновления объявления о встрече."""
import logging

from aiogram.enums import ParseMode
from taskiq import Context, TaskiqDepends

from workers.broker import broker
from templates import AnnouncementTemplates
from config import get_settings
from utils.time import get_tashkent_now

logger = logging.getLogger(__name__)
settings = get_settings()


def get_text_for_day(weekday: int = None, is_final: bool = False) -> str | None:
    """Получить текст для дня недели."""
    if is_final:
        return AnnouncementTemplates.friday_hour_before()

    templates = {
        0: AnnouncementTemplates.monday,
        1: AnnouncementTemplates.tuesday,
        2: AnnouncementTemplates.wednesday,
        3: AnnouncementTemplates.thursday,
        4: AnnouncementTemplates.friday_morning,
    }

    func = templates.get(weekday)
    return func() if func else None


@broker.task(
    schedule=[{
        "cron": "0 10 * * 1-5",  # Пн-Пт 10:00 Ташкент
        "cron_offset": "Asia/Tashkent"
    }]
)
async def update_meeting_announcement(context: Context = TaskiqDepends()) -> bool:
    """Обновить объявление о встрече."""

    now = get_tashkent_now()
    weekday = now.weekday()
    text = get_text_for_day(weekday)

    if not text:
        logger.warning(f"No template for weekday {weekday}")
        return False

    try:
        await context.state.bot.edit_message_caption(
            chat_id=settings.meeting_group_id,
            message_id=settings.announcement_message_id,
            caption=text,
            parse_mode=ParseMode.HTML
        )
        logger.info(f"Updated announcement for weekday {weekday}")
        return True
    except Exception as e:
        logger.error(f"Failed to update announcement: {e}")
        return False


@broker.task(
    schedule=[{
        "cron": "0 13 * * 5",  # Пятница 13:00 Ташкент
        "cron_offset": "Asia/Tashkent"
    }]
)
async def final_meeting_reminder(context: Context = TaskiqDepends()) -> bool:
    """Финальное напоминание за час до встречи."""

    text = get_text_for_day(is_final=True)

    try:
        await context.state.bot.edit_message_caption(
            chat_id=settings.meeting_group_id,
            message_id=settings.announcement_message_id,
            caption=text,
            parse_mode=ParseMode.HTML
        )
        logger.info("Sent final reminder")
        return True
    except Exception as e:
        logger.error(f"Failed to send final reminder: {e}")
        return False
