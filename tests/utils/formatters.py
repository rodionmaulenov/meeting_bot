from utils.formatters import shorten_name


class TestShortenName:
    """Тесты для функции shorten_name"""

    def test_single_word_returns_as_is(self):
        """Одно слово возвращается без изменений"""
        assert shorten_name("Айгуль") == "Айгуль"

    def test_two_words_returns_surname_with_initial(self):
        """Два слова: Фамилия + первая буква имени"""
        assert shorten_name("Каримова Айгуль") == "Каримова А."

    def test_three_words_returns_surname_with_two_initials(self):
        """Три слова: Фамилия + инициалы имени и отчества"""
        assert shorten_name("Руденко Михаил Константинович") == "Руденко М.К."

    def test_long_uzbek_name(self):
        """Длинное узбекское ФИО"""
        assert shorten_name("Абдурахманова Гульнара Рустамовна") == "Абдурахманова Г.Р."

    def test_max_length_truncates_result(self):
        """Результат обрезается по max_length"""
        result = shorten_name("Абдурахманова Гульнара Рустамовна", max_length=10)
        assert len(result) <= 10
        assert result == "Абдурахман"

    def test_single_word_with_max_length(self):
        """Одно длинное слово обрезается"""
        result = shorten_name("Абдурахманова", max_length=5)
        assert result == "Абдур"

    def test_default_max_length_is_32(self):
        """По умолчанию max_length = 32 (лимит Telegram)"""
        # Очень длинное имя
        long_name = "Константинопольский Александр Владимирович"
        result = shorten_name(long_name)
        assert len(result) <= 32