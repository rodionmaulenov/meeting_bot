"""Задача обновления статистики."""
import logging

from taskiq import Context, TaskiqDepends
from aiogram.exceptions import TelegramBadRequest

from workers.broker import broker
from repositories.statistics_repository import StatisticsRepository
from services.statistics_service import StatisticsService
from templates import StatisticsTemplates
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

STATISTICS_MESSAGE_KEY = "meeting:statistics_message_id"


@broker.task(
    schedule=[{
        "cron": "*/5 * * * *",  # Каждые 5 минут
        "cron_offset": "Asia/Tashkent"
    }]
)
async def update_statistics(context: Context = TaskiqDepends()) -> bool:
    """Обновить сообщение со статистикой."""
    try:
        # Инициализация
        repository = StatisticsRepository(supabase=context.state.supabase)
        service = StatisticsService(repository=repository)

        # Получаем статистику
        current_start, current_end = service.get_current_week_range()
        previous_start, previous_end = service.get_previous_week_range()

        current_stats = await service.get_weekly_stats(current_start, current_end)
        previous_stats = await service.get_weekly_stats(previous_start, previous_end)

        # Форматируем текст
        text = StatisticsTemplates.format_full_stats(current_stats, previous_stats)

        # Проверяем есть ли сообщение в Redis
        message_id = await context.state.redis.get(STATISTICS_MESSAGE_KEY)

        if message_id:
            # Редактируем существующее
            try:
                await context.state.bot.edit_message_text(
                    chat_id=settings.commands_group_id,
                    message_id=int(message_id),
                    text=text,
                )
                logger.debug(f"Statistics updated, message_id={message_id}")
            except TelegramBadRequest as e:
                if "is not modified" in e.message:
                    logger.debug(f"Statistics not changed, message_id={message_id}")
                else:
                    # Любая другая BadRequest (удалено, нет прав и т.д.) — создаём новое
                    logger.warning(f"Cannot edit message: {e.message}, creating new")
                    await _create_new_message(context, text)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
        else:
            # Создаём новое
            await _create_new_message(context, text)

        return True

    except Exception as e:
        logger.error(f"Failed to update statistics: {e}")
        return False


async def _create_new_message(context: Context, text: str) -> None:
    """Создать новое сообщение и сохранить ID в Redis."""
    message = await context.state.bot.send_message(
        chat_id=settings.commands_group_id,
        text=text,
    )

    await context.state.redis.set(STATISTICS_MESSAGE_KEY, str(message.message_id))
    logger.debug(f"Statistics created, message_id={message.message_id}")