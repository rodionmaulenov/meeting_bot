from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from templates import (
    ApplicationInstructionsTemplates,
    PhoneTemplates,
    RegionTemplates,
    ChildrenTemplates,
    CesareanTemplates,
    BloodTypeTemplates,
    ConfirmationTemplates,
)


def get_instructions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=ApplicationInstructionsTemplates.btn_confirm(),
                callback_data="instructions:confirm"
            )]
        ]
    )


def get_share_phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=PhoneTemplates.btn_share_phone(),
                request_contact=True
            )]
        ],
        resize_keyboard=True
    )


def get_regions_keyboard() -> InlineKeyboardMarkup:
    regions = RegionTemplates.regions_list()

    keyboard = []
    for i in range(0, len(regions), 2):
        row = [
            InlineKeyboardButton(
                text=regions[i],
                callback_data=f"region:{i}"
            )
        ]
        if i + 1 < len(regions):
            row.append(
                InlineKeyboardButton(
                    text=regions[i + 1],
                    callback_data=f"region:{i + 1}"
                )
            )
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_children_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ChildrenTemplates.btn_no_children(),
                    callback_data="children:0"
                ),
            ],
            [
                InlineKeyboardButton(text="1", callback_data="children:1"),
                InlineKeyboardButton(text="2", callback_data="children:2"),
                InlineKeyboardButton(text="3", callback_data="children:3"),
            ],
            [
                InlineKeyboardButton(text="4", callback_data="children:4"),
                InlineKeyboardButton(text="5", callback_data="children:5"),
                InlineKeyboardButton(
                    text=ChildrenTemplates.btn_more(),
                    callback_data="children:more"
                ),
            ]
        ]
    )


def get_cesarean_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CesareanTemplates.btn_no_cesarean(),
                    callback_data="cesarean:0"
                ),
            ],
            [
                InlineKeyboardButton(text="1", callback_data="cesarean:1"),
                InlineKeyboardButton(text="2", callback_data="cesarean:2"),
                InlineKeyboardButton(
                    text=ChildrenTemplates.btn_more(),
                    callback_data="cesarean:more"
                ),
            ]
        ]
    )


def get_blood_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="I (O)+", callback_data="blood:I+"),
                InlineKeyboardButton(text="I (O)−", callback_data="blood:I-"),
            ],
            [
                InlineKeyboardButton(text="II (A)+", callback_data="blood:II+"),
                InlineKeyboardButton(text="II (A)−", callback_data="blood:II-"),
            ],
            [
                InlineKeyboardButton(text="III (B)+", callback_data="blood:III+"),
                InlineKeyboardButton(text="III (B)−", callback_data="blood:III-"),
            ],
            [
                InlineKeyboardButton(text="IV (AB)+", callback_data="blood:IV+"),
                InlineKeyboardButton(text="IV (AB)−", callback_data="blood:IV-"),
            ],
            [
                InlineKeyboardButton(
                    text=BloodTypeTemplates.btn_blood_type_unknown(),
                    callback_data="blood:unknown"
                ),
            ],
        ]
    )


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_confirm(),
                    callback_data="confirm:yes"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_full_name(),
                    callback_data="edit:full_name"
                ),
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_phones(),
                    callback_data="edit:phones"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_city(),
                    callback_data="edit:city"
                ),
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_age(),
                    callback_data="edit:age"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_height(),
                    callback_data="edit:height"
                ),
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_weight(),
                    callback_data="edit:weight"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_children(),
                    callback_data="edit:children"
                ),
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_cesarean(),
                    callback_data="edit:cesarean"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ConfirmationTemplates.btn_edit_blood_type(),
                    callback_data="edit:blood_type"
                ),
            ],
        ]
    )