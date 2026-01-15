import re

import phonenumbers


def is_valid_phone(phone: str) -> bool:
    """Проверяет валидность номера телефона.

    Номер должен начинаться с + и быть валидным международным номером.
    Поддерживает: Узбекистан, Казахстан, Россия и другие страны.
    """
    if not phone.startswith('+'):
        return False
    try:
        parsed = phonenumbers.parse(phone)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False


def is_valid_full_name(text: str) -> tuple[bool, str | None]:
    """
    Проверка ФИО (только латиница, минимум 2 слова).

    Returns:
        (is_valid, full_name)
    """
    # Только латинские буквы, пробелы, апостроф, дефис
    pattern = r"^[A-Za-z][A-Za-z\s\-']+$"

    if not re.match(pattern, text):
        return False, None

    # Минимум 2 слова (имя и фамилия)
    words = text.split()
    if len(words) < 2:
        return False, None

    return True, text.strip()


def is_valid_age(text: str) -> tuple[bool, int | None, str | None]:
    """
    Проверка возраста.

    Returns:
        (is_valid, age, error_type)
        error_type: "format" | "too_young" | "too_old" | None
    """
    if not text.isdigit():
        return False, None, "format"

    age = int(text)

    if age < 18:
        return False, age, "too_young"

    if age > 39:
        return False, age, "too_old"

    return True, age, None


def is_valid_height(text: str) -> tuple[bool, int | None]:
    """
    Проверка роста (140-200 см).

    Returns:
        (is_valid, height)
    """
    if not text.isdigit():
        return False, None

    height = int(text)

    if height < 140 or height > 200:
        return False, None

    return True, height


def is_valid_weight(text: str) -> tuple[bool, int | None]:
    """
    Проверка веса (40-150 кг).

    Returns:
        (is_valid, weight)
    """
    if not text.isdigit():
        return False, None

    weight = int(text)

    if weight < 40 or weight > 150:
        return False, None

    return True, weight

def is_valid_cesarean(value: str) -> tuple[bool, int | str | None, str | None]:
    """
    Проверка кесарево.

    Returns:
        (is_valid, cesarean, error_type)
        error_type: "too_many" | None
    """
    if value == "more":
        return False, "more", "too_many"

    cesarean = int(value)

    if cesarean >= 2:
        return False, cesarean, "too_many"

    return True, cesarean, None