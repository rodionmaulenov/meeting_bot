from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import get_settings
from services.command_message_service import CommandMessageService

router = Router()
settings = get_settings()


@router.message(Command("clear"), StateFilter("*"))
async def clear_handler(
    message: Message,
    state: FSMContext,
    command_message_service: CommandMessageService
) -> None:
    """Очистить все сообщения бота в топике"""

    # Проверяем что команда в правильном топике
    if message.message_thread_id != settings.commands_thread_id:
        return

    await state.clear()

    await command_message_service.clear_messages()