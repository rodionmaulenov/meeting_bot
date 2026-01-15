"""Handler для сбора анкет в личке бота."""
import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.application import (
    get_instructions_keyboard,
    get_share_phone_keyboard,
    get_regions_keyboard,
    get_children_keyboard,
    get_cesarean_keyboard,
    get_blood_type_keyboard,
    get_confirmation_keyboard,
)
from repositories.application_repository import ApplicationRepository
from repositories.invite_link_repository import InviteLinkRepository
from repositories.member_repository import MemberRepository
from states import ApplicationStates
from templates import (
    ApplicationInstructionsTemplates,
    PhoneTemplates,
    FullNameTemplates,
    RegionTemplates,
    AgeTemplates,
    HeightTemplates,
    WeightTemplates,
    ChildrenTemplates,
    CesareanTemplates,
    BloodTypeTemplates,
    ConfirmationTemplates,
)
from utils.validators import (
    is_valid_phone,
    is_valid_full_name,
    is_valid_age,
    is_valid_height,
    is_valid_weight,
    is_valid_cesarean,
)

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")
router.callback_query.filter(F.message.chat.type == "private")


# ============================================
# СТАРТ АНКЕТЫ
# ============================================

@router.message(CommandStart(deep_link=True))
async def start_application(
        message: Message,
        command: CommandObject,
        state: FSMContext,
        member_repository: MemberRepository,
        application_repository: ApplicationRepository,
        invite_link_repository: InviteLinkRepository,
) -> None:
    """Начало заполнения анкеты по deeplink."""

    if command.args not in ("apply", "reset"):
        return

    if command.args == "apply":
        current_state = await state.get_state()
        if current_state:
            await resume_application(message, state, current_state)
            return

    await state.clear()

    member = await member_repository.get_by_telegram_id(message.from_user.id)

    if not member:
        await message.answer(ApplicationInstructionsTemplates.not_member())
        return

    # Проверяем есть ли уже анкета (включая rejected)
    existing = await application_repository.get_by_member_id(member.id)

    if existing:
        if existing.status == "rejected":
            await message.answer(ApplicationInstructionsTemplates.rejected())
        else:
            await message.answer(ApplicationInstructionsTemplates.already_filled())
        return

    invite_link = await invite_link_repository.get_by_id(member.invite_link_id)

    if not invite_link:
        logger.error(f"Invite link not found for member {member.id}")
        await message.answer("Произошла ошибка. Попробуйте позже.")
        return

    await state.update_data(
        member_id=member.id,
        manager_id=invite_link.manager_id
    )

    await state.set_state(ApplicationStates.waiting_for_confirm)
    await message.answer(
        ApplicationInstructionsTemplates.instructions(),
        reply_markup=get_instructions_keyboard(),
        parse_mode="HTML"
    )


# ============================================
# ИНСТРУКЦИЯ
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_confirm,
    F.data == "instructions:confirm"
)
async def on_instructions_confirm(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Девушка прочитала инструкцию."""

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    await state.set_state(ApplicationStates.waiting_for_telegram_phone)
    await callback.message.answer(
        PhoneTemplates.ask_telegram_phone(),
        reply_markup=get_share_phone_keyboard()
    )


# ============================================
# ТЕЛЕФОНЫ
# ============================================

@router.message(
    ApplicationStates.waiting_for_telegram_phone,
    F.contact
)
async def on_telegram_phone_received(
        message: Message,
        state: FSMContext
) -> None:
    """Девушка поделилась Telegram номером."""

    phone = message.contact.phone_number

    if not phone.startswith("+"):
        phone = f"+{phone}"

    logger.debug(f"Telegram phone: {phone}")

    await state.update_data(telegram_phone=phone)

    await message.answer(
        PhoneTemplates.ask_phone(),
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(ApplicationStates.waiting_for_phones)


@router.message(
    ApplicationStates.waiting_for_phones,
    F.text
)
async def on_phone_received(
        message: Message,
        state: FSMContext
) -> None:
    """Девушка ввела номер для связи."""

    phone = message.text.strip()

    if not is_valid_phone(phone):
        await message.answer(PhoneTemplates.invalid_phone())
        return

    await state.update_data(phones=[phone])
    logger.debug(f"Phone: {phone}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_full_name)
    await message.answer(FullNameTemplates.ask_full_name())


# ============================================
# ФИО
# ============================================

@router.message(
    ApplicationStates.waiting_for_full_name,
    F.text
)
async def on_full_name_received(
        message: Message,
        state: FSMContext
) -> None:
    """Девушка ввела ФИО."""

    is_valid, full_name = is_valid_full_name(message.text.strip())

    if not is_valid:
        await message.answer(FullNameTemplates.invalid_full_name())
        return

    await state.update_data(full_name=full_name)
    logger.debug(f"Full name: {full_name}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_city)
    await message.answer(
        RegionTemplates.ask_city(),
        reply_markup=get_regions_keyboard()
    )


# ============================================
# ОБЛАСТЬ
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_city,
    F.data.startswith("region:")
)
async def on_region_selected(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Девушка выбрала область."""

    index = int(callback.data.split(":")[1])
    regions = RegionTemplates.regions_list()
    city = regions[index]

    await state.update_data(city=city)
    logger.debug(f"City: {city}")

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(callback.message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_age)
    await callback.message.answer(AgeTemplates.ask_age())


# ============================================
# ВОЗРАСТ
# ============================================

@router.message(
    ApplicationStates.waiting_for_age,
    F.text
)
async def on_age_received(
        message: Message,
        state: FSMContext,
        application_repository: ApplicationRepository,
) -> None:
    """Девушка ввела возраст."""

    is_valid, age, error = is_valid_age(message.text.strip())

    if error == "format":
        await message.answer(AgeTemplates.invalid_age_format())
        return

    if error == "too_young":
        await message.answer(AgeTemplates.age_too_young())
        return

    if error == "too_old":
        await message.answer(AgeTemplates.age_too_old())
        await state.update_data(age=age)
        await save_rejected_application(state, application_repository, f"age={age}")
        await state.clear()
        return

    await state.update_data(age=age)
    logger.debug(f"Age: {age}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_height)
    await message.answer(HeightTemplates.ask_height())


# ============================================
# РОСТ
# ============================================

@router.message(
    ApplicationStates.waiting_for_height,
    F.text
)
async def on_height_received(
        message: Message,
        state: FSMContext
) -> None:
    """Девушка ввела рост."""

    is_valid, height = is_valid_height(message.text.strip())

    if not is_valid:
        await message.answer(HeightTemplates.invalid_height())
        return

    await state.update_data(height=height)
    logger.debug(f"Height: {height}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_weight)
    await message.answer(WeightTemplates.ask_weight())


# ============================================
# ВЕС
# ============================================

@router.message(
    ApplicationStates.waiting_for_weight,
    F.text
)
async def on_weight_received(
        message: Message,
        state: FSMContext
) -> None:
    """Девушка ввела вес."""

    is_valid, weight = is_valid_weight(message.text.strip())

    if not is_valid:
        await message.answer(WeightTemplates.invalid_weight())
        return

    await state.update_data(weight=weight)
    logger.debug(f"Weight: {weight}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_children)
    await message.answer(
        ChildrenTemplates.ask_children(),
        reply_markup=get_children_keyboard()
    )


# ============================================
# ДЕТИ
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_children,
    F.data.startswith("children:")
)
async def on_children_selected(
        callback: CallbackQuery,
        state: FSMContext,
        application_repository: ApplicationRepository,
) -> None:
    """Девушка выбрала количество детей."""

    value = callback.data.split(":")[1]

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    # Отказ если нет детей
    if value == "0":
        await callback.message.answer(ChildrenTemplates.no_children_rejected())
        await state.update_data(children="0")
        await save_rejected_application(state, application_repository, "no_children")
        await state.clear()
        return

    if value == "more":
        children = "more"
    else:
        children = int(value)

    await state.update_data(children=children)
    logger.debug(f"Children: {children}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(callback.message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_cesarean)
    await callback.message.answer(
        CesareanTemplates.ask_cesarean(),
        reply_markup=get_cesarean_keyboard()
    )


# ============================================
# КЕСАРЕВО
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_cesarean,
    F.data.startswith("cesarean:")
)
async def on_cesarean_selected(
        callback: CallbackQuery,
        state: FSMContext,
        application_repository: ApplicationRepository,
) -> None:
    """Девушка выбрала количество кесаревых."""

    value = callback.data.split(":")[1]

    is_valid, cesarean, error = is_valid_cesarean(value)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    if error == "too_many":
        await callback.message.answer(CesareanTemplates.cesarean_too_many())
        await state.update_data(cesarean=cesarean)
        await save_rejected_application(state, application_repository, f"cesarean={cesarean}")
        await state.clear()
        return

    await state.update_data(cesarean=cesarean)
    logger.debug(f"Cesarean: {cesarean}")

    data = await state.get_data()
    if data.get("editing"):
        await return_to_confirmation(callback.message, state)
        return

    await state.set_state(ApplicationStates.waiting_for_blood_type)
    await callback.message.answer(
        BloodTypeTemplates.ask_blood_type(),
        reply_markup=get_blood_type_keyboard()
    )


# ============================================
# ГРУППА КРОВИ
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_blood_type,
    F.data.startswith("blood:")
)
async def on_blood_type_selected(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Девушка выбрала группу крови."""

    blood_type = callback.data.split(":")[1]

    await state.update_data(blood_type=blood_type)
    logger.debug(f"Blood type: {blood_type}")

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    data = await state.get_data()
    await state.set_state(ApplicationStates.waiting_for_confirmation)
    await callback.message.answer(
        ConfirmationTemplates.show_summary(data),
        reply_markup=get_confirmation_keyboard()
    )


# ============================================
# ПОДТВЕРЖДЕНИЕ
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_confirmation,
    F.data == "confirm:yes"
)
async def on_application_confirmed(
        callback: CallbackQuery,
        state: FSMContext,
        application_repository: ApplicationRepository,
) -> None:
    """Девушка подтвердила анкету."""

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    data = await state.get_data()

    logger.debug(
        f"Application data: "
        f"member_id={data['member_id']}, "
        f"manager_id={data['manager_id']}, "
        f"full_name={data['full_name']}, "
        f"telegram_phone={data['telegram_phone']}, "
        f"phones={data['phones']}, "
        f"city={data['city']}, "
        f"age={data['age']}, "
        f"height={data['height']}, "
        f"weight={data['weight']}, "
        f"children={data['children']}, "
        f"cesarean={data['cesarean']}, "
        f"blood_type={data['blood_type']}"
    )

    await application_repository.create(
        member_id=data["member_id"],
        manager_id=data["manager_id"],
        full_name=data["full_name"],
        telegram_phone=data["telegram_phone"],
        phones=data["phones"],
        city=data["city"],
        age=data["age"],
        height=data["height"],
        weight=data["weight"],
        children=data["children"],
        cesarean=data["cesarean"],
        blood_type=data["blood_type"],
        status="completed",
    )

    logger.info(f"Application saved: member_id={data['member_id']}")

    await callback.message.answer(ConfirmationTemplates.application_saved())
    await state.clear()


# ============================================
# РЕДАКТИРОВАНИЕ ПОЛЕЙ
# ============================================

@router.callback_query(
    ApplicationStates.waiting_for_confirmation,
    F.data.startswith("edit:")
)
async def on_edit_field(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Девушка хочет изменить поле."""

    field = callback.data.split(":")[1]

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    await state.update_data(editing=True)

    if field == "full_name":
        await state.set_state(ApplicationStates.waiting_for_full_name)
        await callback.message.answer(FullNameTemplates.ask_full_name())

    elif field == "phones":
        await state.update_data(phones=[])
        await state.set_state(ApplicationStates.waiting_for_phones)
        await callback.message.answer(PhoneTemplates.ask_phone())

    elif field == "city":
        await state.set_state(ApplicationStates.waiting_for_city)
        await callback.message.answer(
            RegionTemplates.ask_city(),
            reply_markup=get_regions_keyboard()
        )

    elif field == "age":
        await state.set_state(ApplicationStates.waiting_for_age)
        await callback.message.answer(AgeTemplates.ask_age())

    elif field == "height":
        await state.set_state(ApplicationStates.waiting_for_height)
        await callback.message.answer(HeightTemplates.ask_height())

    elif field == "weight":
        await state.set_state(ApplicationStates.waiting_for_weight)
        await callback.message.answer(WeightTemplates.ask_weight())

    elif field == "children":
        await state.set_state(ApplicationStates.waiting_for_children)
        await callback.message.answer(
            ChildrenTemplates.ask_children(),
            reply_markup=get_children_keyboard()
        )

    elif field == "cesarean":
        await state.set_state(ApplicationStates.waiting_for_cesarean)
        await callback.message.answer(
            CesareanTemplates.ask_cesarean(),
            reply_markup=get_cesarean_keyboard()
        )

    elif field == "blood_type":
        await state.set_state(ApplicationStates.waiting_for_blood_type)
        await callback.message.answer(
            BloodTypeTemplates.ask_blood_type(),
            reply_markup=get_blood_type_keyboard()
        )


# ============================================
# HELPER ФУНКЦИИ
# ============================================

async def return_to_confirmation(
        message: Message,
        state: FSMContext
) -> None:
    """Возврат к экрану подтверждения после редактирования."""

    data = await state.get_data()
    await state.update_data(editing=False)
    await state.set_state(ApplicationStates.waiting_for_confirmation)
    await message.answer(
        ConfirmationTemplates.show_summary(data),
        reply_markup=get_confirmation_keyboard()
    )


async def resume_application(
        message: Message,
        state: FSMContext,
        current_state: str
) -> None:
    """Возврат к текущему этапу анкеты."""

    if current_state == ApplicationStates.waiting_for_confirm:
        await message.answer(
            ApplicationInstructionsTemplates.instructions(),
            reply_markup=get_instructions_keyboard(),
            parse_mode="HTML"
        )

    elif current_state == ApplicationStates.waiting_for_telegram_phone:
        await message.answer(
            PhoneTemplates.ask_telegram_phone(),
            reply_markup=get_share_phone_keyboard()
        )

    elif current_state == ApplicationStates.waiting_for_phones:
        await message.answer(PhoneTemplates.ask_phone())

    elif current_state == ApplicationStates.waiting_for_full_name:
        await message.answer(FullNameTemplates.ask_full_name())

    elif current_state == ApplicationStates.waiting_for_city:
        await message.answer(
            RegionTemplates.ask_city(),
            reply_markup=get_regions_keyboard()
        )

    elif current_state == ApplicationStates.waiting_for_age:
        await message.answer(AgeTemplates.ask_age())

    elif current_state == ApplicationStates.waiting_for_height:
        await message.answer(HeightTemplates.ask_height())

    elif current_state == ApplicationStates.waiting_for_weight:
        await message.answer(WeightTemplates.ask_weight())

    elif current_state == ApplicationStates.waiting_for_children:
        await message.answer(
            ChildrenTemplates.ask_children(),
            reply_markup=get_children_keyboard()
        )

    elif current_state == ApplicationStates.waiting_for_cesarean:
        await message.answer(
            CesareanTemplates.ask_cesarean(),
            reply_markup=get_cesarean_keyboard()
        )

    elif current_state == ApplicationStates.waiting_for_blood_type:
        await message.answer(
            BloodTypeTemplates.ask_blood_type(),
            reply_markup=get_blood_type_keyboard()
        )

    elif current_state == ApplicationStates.waiting_for_confirmation:
        data = await state.get_data()
        await message.answer(
            ConfirmationTemplates.show_summary(data),
            reply_markup=get_confirmation_keyboard()
        )

    else:
        await message.answer("Продолжаем заполнение анкеты...")


# ============================================
# При reject сохраняем все введённые данные
# ============================================

async def save_rejected_application(
        state: FSMContext,
        application_repository: ApplicationRepository,
        reason: str,
) -> None:
    """Сохраняет rejected анкету с теми данными, которые успели ввести."""

    data = await state.get_data()

    await application_repository.create(
        member_id=data.get("member_id"),
        manager_id=data.get("manager_id"),
        full_name=data.get("full_name"),
        telegram_phone=data.get("telegram_phone"),
        phones=data.get("phones", []),
        city=data.get("city"),
        age=data.get("age"),
        height=data.get("height"),
        weight=data.get("weight"),
        children=data.get("children"),
        cesarean=data.get("cesarean"),
        blood_type=data.get("blood_type"),
        status="rejected",
    )

    logger.info(f"Application rejected ({reason}): member_id={data.get('member_id')}")
