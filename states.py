from aiogram.fsm.state import State, StatesGroup


class AddGirlStates(StatesGroup):
    waiting_for_name = State()

class ApplicationStates(StatesGroup):
    waiting_for_confirm = State()
    waiting_for_telegram_phone = State()
    waiting_for_phones = State()
    waiting_for_full_name = State()
    waiting_for_city = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_children = State()
    waiting_for_cesarean = State()
    waiting_for_blood_type = State()
    waiting_for_confirmation = State()