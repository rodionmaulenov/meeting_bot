"""Задача планирования Video Chat."""
import logging
from datetime import timedelta

from taskiq import Context, TaskiqDepends

from workers.broker import broker
from services.video_chat_service import VideoChatService
from utils.time import get_tashkent_now
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@broker.task(
    schedule=[{
        "cron": "0 14 * * 4",  # Четверг 14:00 Ташкент
        "cron_offset": "Asia/Tashkent"
    }]
)
async def schedule_video_chat(context: Context = TaskiqDepends()) -> str | None:
    """Запланировать Video Chat на завтра (пятницу) в 14:00 Ташкент."""

    # 1. Вычисляем время встречи — завтра 14:00 Ташкент
    now = get_tashkent_now()
    tomorrow = now + timedelta(days=1)
    meeting_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)

    # 2. Создаём сервис
    video_chat_service = VideoChatService(
        client=context.state.userbot,
        redis=context.state.redis,
        group_id=settings.meeting_group_id
    )

    # 3. Планируем Video Chat
    link = await video_chat_service.schedule_video_chat(
        schedule_date=meeting_time,
        title="Еженедельная встреча"
    )

    if link:
        logger.info(f"Video chat scheduled for {meeting_time}, link: {link}")
    else:
        logger.error("Failed to schedule video chat")

    return link
