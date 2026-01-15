"""Шаблоны сообщений для бота. Легко переводить на другие языки."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.statistics_service import WeeklyStats, ManagerStats


class InviteLinkTemplates:
    """Шаблоны для invite-ссылок"""

    @staticmethod
    def link_created(member_name: str, invite_link: str) -> str:
        return (
            f"✅ Ссылка для: {member_name}\n\n"
            f"⏰ Действует: 24 часа\n"
            f"👤 Можно использовать только один раз\n\n"
            f"<code>{invite_link}</code>\n\n"
            f"👆 Нажми на ссылку и скопируй"
        )

    @staticmethod
    def enter_name() -> str:
        return "📝 Введите ФИО участницы:"

    @staticmethod
    def access_forbidden() -> str:
        return "❌ У вас нет прав для создания ссылок"


class RestrictionTemplate:

    @staticmethod
    def you_are_not_manager() -> str:
        return "❌ у тебя нет прав на работу."


class AnnouncementTemplates:
    INSTAGRAM = "https://instagram.com/biotexcom.uz.clinic"
    TELEGRAM = "https://t.me/biotexcom_uz"

    @staticmethod
    def header() -> str:
        return (
            "💡 <b>Как не пропустить встречу?</b>\n"
            "Нажмите на панель видеочата сверху и выберите "
            "«Menga xabar qilish» (Notify me) — получите уведомление перед началом.\n"
            "Когда встреча начнётся, нажмите «Qo'shilish» (Join) чтобы войти.\n"
            "👆 Смотрите фото выше\n\n"
            "━━━━━━━━━━━━━━━\n\n"
        )

    @staticmethod
    def footer() -> str:
        return (
            "\n\n━━━━━━━━━━━━━━━\n"
            f"📸 <a href='{AnnouncementTemplates.INSTAGRAM}'>Наш Instagram</a> | "
            f"📱 <a href='{AnnouncementTemplates.TELEGRAM}'>Наш Telegram</a>"
        )

    @staticmethod
    def monday() -> str:
        return (
                AnnouncementTemplates.header()
                + "👋 <b>Добро пожаловать!</b>\n\n"
                  "В эту пятницу в 14:00 состоится видеовстреча.\n\n"
                  "<b>На встрече вы сможете:</b>\n"
                  "• Познакомиться с нашей командой\n"
                  "• Задать любые вопросы\n"
                  "• Узнать подробности о программе\n\n"
                  "📅 <b>До встречи 5 дней</b>"
                + AnnouncementTemplates.footer()
        )

    @staticmethod
    def tuesday() -> str:
        return (
                AnnouncementTemplates.header()
                + "🎥 <b>Видеовстреча в пятницу в 14:00</b>\n\n"
                  "Если у вас есть вопросы — запишите их, "
                  "чтобы не забыть спросить на встрече.\n\n"
                  "📅 <b>До встречи 4 дня</b>"
                + AnnouncementTemplates.footer()
        )

    @staticmethod
    def wednesday() -> str:
        return (
                AnnouncementTemplates.header()
                + "🎥 <b>Видеовстреча в пятницу в 14:00</b>\n\n"
                  "Половина недели позади!\n"
                  "Ждём вас на встрече 💜\n\n"
                  "📅 <b>До встречи 3 дня</b>"
                + AnnouncementTemplates.footer()
        )

    @staticmethod
    def thursday() -> str:
        return (
                AnnouncementTemplates.header()
                + "🎥 <b>Видеовстреча уже завтра!</b>\n\n"
                  "📅 <b>До встречи 1 день</b>"
                + AnnouncementTemplates.footer()
        )

    @staticmethod
    def friday_morning() -> str:
        return (
                AnnouncementTemplates.header()
                + "🎥 <b>Сегодня в 14:00 — видеовстреча!</b>\n\n"
                  "Осталось несколько часов.\n"
                  "До скорой встречи! 💜\n\n"
                  "📅 <b>Встреча сегодня</b>"
                + AnnouncementTemplates.footer()
        )

    @staticmethod
    def friday_hour_before() -> str:
        return (
                AnnouncementTemplates.header()
                + "🔔 <b>Встреча через час!</b>\n\n"
                  "В 14:00 начинаем.\n"
                  "Ждём вас! 💜\n\n"
                  "📅 <b>Встреча в 14:00</b>"
                + AnnouncementTemplates.footer()
        )


class ApplicationMessageTemplates:
    """Сообщение в группе с кнопкой анкеты"""

    @staticmethod
    def message() -> str:
        return (
            "💜 Спасибо, что были с нами на встрече!\n\n"
            "Хотите попасть в программу? Заполните короткую анкету — "
            "это займёт пару минут.\n\n"
            "📝 Спросим: город, возраст, рост, вес, количество детей, "
            "группу крови и номер телефона.\n\n"
            "🔒 Все данные конфиденциальны."
        )

    @staticmethod
    def button_text() -> str:
        return "📋 Заполнить анкету"


class ApplicationInstructionsTemplates:
    """Инструкция и ошибки доступа"""

    @staticmethod
    def instructions() -> str:
        return (
            "📋 Как заполнить анкету\n\n"
            "1️⃣ Telegram номер\n"
            "Нажмите кнопку «Поделиться номером» — это безопасно, номер виден только нам.\n\n"
            "2️⃣ Номер для связи\n"
            "Введите номер с + в начале.\n"
            "Пример: +998901234567\n\n"
            "3️⃣ ФИО, область, возраст, рост, вес\n"
            "Просто напишите текстом. Рост в см, вес в кг.\n\n"
            "4️⃣ Количество детей, кесарево и группа крови\n"
            "Выберите нужный вариант кнопкой.\n\n"
            "—\n\n"
            "✏️ После заполнения вы увидите все свои данные и сможете изменить любое поле.\n"
            "На проверку и редактирование у вас будет 5 минут.\n\n"
            "🔄 Застряли или хотите начать заново?\n"
            "<a href='https://t.me/surrogacy_meeting_bot?start=reset'>Нажмите сюда</a> — все данные сбросятся"
            " и заполнение анкеты начнётся с начала."
        )

    @staticmethod
    def not_member() -> str:
        return (
            "❌ Вы не являетесь участницей группы.\n\n"
            "Чтобы заполнить анкету, сначала нужно вступить в группу по приглашению от менеджера."
        )

    @staticmethod
    def already_filled() -> str:
        return (
            "✅ Вы уже заполнили анкету.\n\n"
            "Наш менеджер свяжется с вами в ближайшее время."
        )

    @staticmethod
    def rejected() -> str:
        return (
            "❌ К сожалению, вы не можете участвовать в программе.\n\n"
            "Если считаете что это ошибка — свяжитесь с менеджером."
        )

    @staticmethod
    def btn_confirm() -> str:
        return "Понятно ✓"


class PhoneTemplates:
    """Телефоны"""

    @staticmethod
    def ask_telegram_phone() -> str:
        return (
            "📱 Поделитесь вашим Telegram номером.\n\n"
            "Это безопасно — номер виден только нам."
        )

    @staticmethod
    def btn_share_phone() -> str:
        return "📱 Поделиться номером"

    @staticmethod
    def ask_phone() -> str:
        return (
            "📞 Введите мобильный номер, по которому вам можно позвонить.\n\n"
            "Формат: +998XXXXXXXXX\n"
            "Пример: +998901234567"
        )

    @staticmethod
    def invalid_phone() -> str:
        return (
            "❌ Неверный формат.\n\n"
            "Введите номер с + в начале.\n"
            "Пример: +998901234567"
        )


class FullNameTemplates:
    """ФИО"""

    @staticmethod
    def ask_full_name() -> str:
        return (
            "👤 Введите ваше полное имя латиницей:\n"
            "Фамилия Имя Отчество\n\n"
            "Пример: Karimova Malika Rustamovna"
        )

    @staticmethod
    def invalid_full_name() -> str:
        return (
            "❌ Пожалуйста, введите ФИО латинскими буквами.\n\n"
            "Пример: Karimova Malika Rustamovna"
        )


class RegionTemplates:
    """Область"""

    @staticmethod
    def regions_list() -> list[str]:
        return [
            "Ташкентская",
            "Самаркандская",
            "Бухарская",
            "Ферганская",
            "Андижанская",
            "Наманганская",
            "Кашкадарьинская",
            "Сурхандарьинская",
            "Хорезмская",
            "Навоийская",
            "Джизакская",
            "Сырдарьинская",
            "Каракалпакстан",
            "г. Ташкент",
        ]

    @staticmethod
    def ask_city() -> str:
        return "🏙 В какой области вы живёте?"


class AgeTemplates:
    """Возраст"""

    @staticmethod
    def ask_age() -> str:
        return "📅 Сколько вам полных лет?"

    @staticmethod
    def invalid_age_format() -> str:
        return "❌ Пожалуйста, введите только число.\nПример: 25"

    @staticmethod
    def age_too_young() -> str:
        return "❌ К сожалению, участвовать в программе можно только с 18 лет."

    @staticmethod
    def age_too_old() -> str:
        return (
            "😔 К сожалению, мы не можем записать вас в программу.\n\n"
            "По медицинским требованиям возраст участниц — до 40 лет.\n"
            "Спасибо за интерес к программе!"
        )


class HeightTemplates:
    """Рост"""

    @staticmethod
    def ask_height() -> str:
        return "📏 Ваш рост в сантиметрах?\nПример: 165"

    @staticmethod
    def invalid_height() -> str:
        return "❌ Введите число от 140 до 200.\nПример: 165"


class WeightTemplates:
    """Вес"""

    @staticmethod
    def ask_weight() -> str:
        return "⚖️ Ваш вес в килограммах?\nПример: 55"

    @staticmethod
    def invalid_weight() -> str:
        return "❌ Введите число от 40 до 150.\nПример: 55"


class ChildrenTemplates:
    """Дети"""

    @staticmethod
    def ask_children() -> str:
        return "👶 Сколько у вас детей?"

    @staticmethod
    def btn_no_children() -> str:
        return "Нет детей"

    @staticmethod
    def btn_more() -> str:
        return "Больше"

    @staticmethod
    def no_children_rejected() -> str:
        return (
            "😔 К сожалению, мы не можем записать вас в программу.\n\n"
            "Для участия необходимо иметь хотя бы одного ребёнка.\n"
            "Спасибо за интерес к программе!"
        )


class CesareanTemplates:
    """Кесарево"""

    @staticmethod
    def ask_cesarean() -> str:
        return "🏥 Сколько раз было кесарево сечение?"

    @staticmethod
    def btn_no_cesarean() -> str:
        return "Не было"

    @staticmethod
    def cesarean_too_many() -> str:
        return (
            "😔 К сожалению, мы не можем записать вас в программу.\n\n"
            "По медицинским требованиям участвовать могут женщины с не более чем 1 кесаревым сечением.\n"
            "Это связано с рисками для вашего здоровья.\n\n"
            "Спасибо за интерес к программе!"
        )


class BloodTypeTemplates:
    """Группа крови"""

    @staticmethod
    def ask_blood_type() -> str:
        return "🩸 Какая у вас группа крови?"

    @staticmethod
    def btn_blood_type_unknown() -> str:
        return "Не знаю"


class ConfirmationTemplates:
    """Подтверждение анкеты"""

    @staticmethod
    def show_summary(data: dict) -> str:
        phones = ", ".join(data.get("phones", []))

        children = data.get("children")
        if children == "more":
            children_text = "больше 5"
        else:
            children_text = str(children)

        cesarean = data.get("cesarean")
        if cesarean == 0:
            cesarean_text = "не было"
        else:
            cesarean_text = str(cesarean)

        blood = data.get("blood_type")
        if blood == "unknown":
            blood_text = "не знаю"
        else:
            blood_text = blood

        return (
            "📋 Проверьте ваши данные:\n\n"
            f"👤 ФИО: {data.get('full_name')}\n"
            f"📱 Telegram: {data.get('telegram_phone')}\n"
            f"📞 Телефон: {phones}\n"
            f"🏙 Область: {data.get('city')}\n"
            f"📅 Возраст: {data.get('age')}\n"
            f"📏 Рост: {data.get('height')} см\n"
            f"⚖️ Вес: {data.get('weight')} кг\n"
            f"👶 Дети: {children_text}\n"
            f"🏥 Кесарево: {cesarean_text}\n"
            f"🩸 Группа крови: {blood_text}\n\n"
            "Всё верно? Нажмите «Подтвердить» или выберите поле для изменения."
        )

    @staticmethod
    def btn_confirm() -> str:
        return "✅ Подтвердить"

    @staticmethod
    def btn_edit_full_name() -> str:
        return "👤 ФИО"

    @staticmethod
    def btn_edit_phones() -> str:
        return "📞 Телефон"

    @staticmethod
    def btn_edit_city() -> str:
        return "🏙 Область"

    @staticmethod
    def btn_edit_age() -> str:
        return "📅 Возраст"

    @staticmethod
    def btn_edit_height() -> str:
        return "📏 Рост"

    @staticmethod
    def btn_edit_weight() -> str:
        return "⚖️ Вес"

    @staticmethod
    def btn_edit_children() -> str:
        return "👶 Дети"

    @staticmethod
    def btn_edit_cesarean() -> str:
        return "🏥 Кесарево"

    @staticmethod
    def btn_edit_blood_type() -> str:
        return "🩸 Группа крови"

    @staticmethod
    def application_saved() -> str:
        return (
            "✅ Анкета успешно сохранена!\n\n"
            "Наш менеджер свяжется с вами в ближайшее время.\n"
            "Спасибо за интерес к программе! 💜"
        )


class StatisticsTemplates:
    """Шаблоны для статистики."""

    @staticmethod
    def format_full_stats(
            current_week: "WeeklyStats",
            previous_week: "WeeklyStats"
    ) -> str:
        """Форматировать полную статистику."""
        from utils.time import get_tashkent_now

        current = StatisticsTemplates._format_week(current_week, "Эта неделя")
        previous = StatisticsTemplates._format_week(previous_week, "Прошлая неделя")

        now = get_tashkent_now()
        updated = now.strftime("%d.%m.%Y %H:%M")

        return (
            f"{current}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{previous}"
            f"🕐 Обновлено: {updated}"
        )

    @staticmethod
    def _format_week(stats: "WeeklyStats", title: str) -> str:
        """Форматировать одну неделю."""
        start = stats.start_date.strftime("%d.%m")
        end = stats.end_date.strftime("%d.%m")

        lines = [f"📊 {title} ({start} — {end})\n"]

        for m in stats.managers:
            lines.append(StatisticsTemplates._format_manager(m))

        lines.append(StatisticsTemplates._format_totals(stats))

        return "\n".join(lines) + "\n"

    @staticmethod
    def _format_manager(m: "ManagerStats") -> str:
        """Форматировать статистику менеджера."""
        lines = [f"👤 {m.manager_name}", f"   Привела: {m.members_count}"]

        # Видео
        if m.video_count > 0:
            lines.append(f"   Видео: {m.video_count} ({m.video_percent}%)")
        else:
            lines.append("   Видео: —")

        # Ср. время
        if m.avg_duration_minutes is not None:
            lines.append(f"   Ср. время: {m.avg_duration_minutes} мин")
        else:
            lines.append("   Ср. время: —")

        # Анкеты
        if m.completed_count > 0 or m.rejected_count > 0:
            lines.append(f"   Анкеты: ✅ {m.completed_count} ❌ {m.rejected_count}")
        else:
            lines.append("   Анкеты: —")

        return "\n".join(lines) + "\n"

    @staticmethod
    def _format_totals(stats: "WeeklyStats") -> str:
        """Форматировать итого."""
        lines = ["📈 Итого:", f"   Новых: {stats.total_members}"]

        if stats.total_video > 0:
            lines.append(f"   Видео: {stats.total_video} ({stats.total_video_percent}%)")
        else:
            lines.append("   Видео: —")

        if stats.total_completed > 0 or stats.total_rejected > 0:
            lines.append(f"   Анкеты: ✅ {stats.total_completed} ❌ {stats.total_rejected}")
        else:
            lines.append("   Анкеты: —")

        return "\n".join(lines)
