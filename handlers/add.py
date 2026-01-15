from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import get_settings
from services.invite_link_service import InviteLinkService
from states import AddGirlStates
from templates import InviteLinkTemplates

router = Router()
settings = get_settings()


@router.message(Command("add"), StateFilter("*"))
async def add_command(
        message: Message,
        state: FSMContext
) -> Message | None:
    """Шаг 1: Менеджер вводит /add"""

    if message.message_thread_id != settings.commands_thread_id:
        return None

    await state.set_state(AddGirlStates.waiting_for_name)

    return await message.reply(InviteLinkTemplates.enter_name())


@router.message(AddGirlStates.waiting_for_name)
async def name_received(
        message: Message,
        state: FSMContext,
        invite_link_service: InviteLinkService
) -> Message:
    """Шаг 2: Менеджер вводит ФИО"""

    member_name = message.text.strip()

    try:
        invite_link = await invite_link_service.create_invite_link(
            manager_telegram_id=message.from_user.id,
            member_name=member_name
        )
    except ValueError:
        await state.clear()
        return await message.reply(InviteLinkTemplates.access_forbidden())

    await state.clear()

    return await message.answer(
        InviteLinkTemplates.link_created(member_name, invite_link.link),
        parse_mode="HTML"
    )