def shorten_name(full_name: str, max_length: int = 32) -> str:
    """
    Сокращает ФИО: фамилия полностью, остальное — инициалы.

    "Руденко Михаил Константинович" → "Руденко М.К."
    "Абдурахманова Гульнара Рустамовна" → "Абдурахманова Г.Р."
    "Айгуль Каримова" → "Каримова А."
    """
    parts = full_name.split()

    if len(parts) == 1:
        # Только фамилия
        return full_name[:max_length]

    if len(parts) == 2:
        # Фамилия + Имя → Фамилия И.
        surname = parts[0]
        name_initial = parts[1][0] + "."
        return f"{surname} {name_initial}"[:max_length]

    # Фамилия + Имя + Отчество → Фамилия И.О.
    surname = parts[0]
    name_initial = parts[1][0] + "."
    patronymic_initial = parts[2][0] + "."

    return f"{surname} {name_initial}{patronymic_initial}"[:max_length]