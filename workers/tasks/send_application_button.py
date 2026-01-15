"""Задача отправки кнопки анкеты в группу."""
import json
import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from taskiq import Context, TaskiqDepends

from workers.broker import broker
from templates import ApplicationMessageTemplates
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

REDIS_KEY = "meeting_bot:application_message"
REDIS_TTL = 345600  # 4 дня


@broker.task(
    schedule=[{
        "cron": "0 14 * * 5",  # Пятница 14:00 Ташкент
        "cron_offset": "Asia/Tashkent"
    }]
)
async def send_application_button(context: Context = TaskiqDepends()) -> int | None:
    """Отправить сообщение с кнопкой анкеты в группу."""

    deeplink = f"https://t.me/{settings.bot_username}?start=apply"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ApplicationMessageTemplates.button_text(), url=deeplink)]
        ]
    )

    try:
        message = await context.state.bot.send_message(
            chat_id=settings.meeting_group_id,
            text=ApplicationMessageTemplates.message(),
            reply_markup=keyboard
        )

        # Сохраняем message_id в Redis для удаления в cleanup
        await context.state.redis.set(
            REDIS_KEY,
            json.dumps({"message_id": message.message_id}),
            ex=REDIS_TTL
        )

        logger.debug(f"Sent application button message: {message.message_id}")
        return message.message_id

    except Exception as e:
        logger.error(f"Failed to send application button: {e}")
        return None