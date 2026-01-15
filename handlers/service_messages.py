"""Удаление служебных сообщений в Meeting Group."""
import logging
from aiogram import Router, F
from aiogram.types import Message

from config import get_settings

logger = logging.getLogger(__name__)
router = Router()
settings = get_settings()

# Все служебные сообщения
SERVICE_FILTER = (
    F.new_chat_members |                    # "Айгуль joined"
    F.left_chat_member |                    # "Айгуль left"
    F.video_chat_scheduled |                # "Video chat scheduled"
    F.video_chat_started |                  # "Video chat started"
    F.video_chat_ended |                    # "Video chat ended"
    F.video_chat_participants_invited |     # "X invited Y to video chat"
    F.pinned_message |                      # "Message pinned"
    F.new_chat_title |                      # "Chat renamed"
    F.new_chat_photo |                      # "Chat photo changed"
    F.delete_chat_photo                     # "Chat photo deleted"
)


@router.message(
    SERVICE_FILTER,
    F.chat.id == settings.meeting_group_id,
)
async def delete_service_messages(message: Message) -> None:
    """Удаляет служебные сообщения в Meeting Group."""
    try:
        await message.delete()
        logger.debug(f"Deleted service message {message.message_id}")
    except Exception as e:
        logger.warning(f"Could not delete service message: {e}")