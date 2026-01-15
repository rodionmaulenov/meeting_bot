"""Тесты для валидаторов."""
from utils.validators import (
    is_valid_phone,
    is_valid_full_name,
    is_valid_age,
    is_valid_height,
    is_valid_weight,
    is_valid_cesarean,
)


class TestIsValidPhone:
    """Тесты для is_valid_phone."""

    def test_valid_uzbekistan_phone(self):
        assert is_valid_phone("+998901234567") is True

    def test_valid_kazakhstan_phone(self):
        assert is_valid_phone("+77011234567") is True

    def test_valid_russia_phone(self):
        assert is_valid_phone("+79161234567") is True

    def test_invalid_without_plus(self):
        assert is_valid_phone("998901234567") is False

    def test_invalid_short_number(self):
        assert is_valid_phone("+99890123") is False

    def test_invalid_letters(self):
        assert is_valid_phone("+998abc1234567") is False

    def test_invalid_empty(self):
        assert is_valid_phone("") is False


class TestIsValidFullName:
    """Тесты для is_valid_full_name."""

    def test_valid_full_name(self):
        is_valid, name = is_valid_full_name("Karimova Malika Rustamovna")
        assert is_valid is True
        assert name == "Karimova Malika Rustamovna"

    def test_valid_two_words(self):
        is_valid, name = is_valid_full_name("Karimova Malika")
        assert is_valid is True
        assert name == "Karimova Malika"

    def test_valid_with_apostrophe(self):
        is_valid, name = is_valid_full_name("O'Connor John")
        assert is_valid is True

    def test_valid_with_hyphen(self):
        is_valid, name = is_valid_full_name("Mary-Jane Watson")
        assert is_valid is True

    def test_invalid_cyrillic(self):
        is_valid, name = is_valid_full_name("Каримова Малика")
        assert is_valid is False
        assert name is None

    def test_invalid_single_word(self):
        is_valid, name = is_valid_full_name("Karimova")
        assert is_valid is False
        assert name is None

    def test_invalid_with_numbers(self):
        is_valid, name = is_valid_full_name("Karimova123 Malika")
        assert is_valid is False

    def test_invalid_empty(self):
        is_valid, name = is_valid_full_name("")
        assert is_valid is False


class TestIsValidAge:
    """Тесты для is_valid_age."""

    def test_valid_age_18(self):
        is_valid, age, error = is_valid_age("18")
        assert is_valid is True
        assert age == 18
        assert error is None

    def test_valid_age_39(self):
        is_valid, age, error = is_valid_age("39")
        assert is_valid is True
        assert age == 39
        assert error is None

    def test_valid_age_25(self):
        is_valid, age, error = is_valid_age("25")
        assert is_valid is True
        assert age == 25

    def test_invalid_too_young(self):
        is_valid, age, error = is_valid_age("17")
        assert is_valid is False
        assert age == 17
        assert error == "too_young"

    def test_invalid_too_old(self):
        is_valid, age, error = is_valid_age("40")
        assert is_valid is False
        assert age == 40
        assert error == "too_old"

    def test_invalid_format_letters(self):
        is_valid, age, error = is_valid_age("abc")
        assert is_valid is False
        assert age is None
        assert error == "format"

    def test_invalid_format_mixed(self):
        is_valid, age, error = is_valid_age("25лет")
        assert is_valid is False
        assert error == "format"


class TestIsValidHeight:
    """Тесты для is_valid_height."""

    def test_valid_height_min(self):
        is_valid, height = is_valid_height("140")
        assert is_valid is True
        assert height == 140

    def test_valid_height_max(self):
        is_valid, height = is_valid_height("200")
        assert is_valid is True
        assert height == 200

    def test_valid_height_normal(self):
        is_valid, height = is_valid_height("165")
        assert is_valid is True
        assert height == 165

    def test_invalid_too_short(self):
        is_valid, height = is_valid_height("139")
        assert is_valid is False
        assert height is None

    def test_invalid_too_tall(self):
        is_valid, height = is_valid_height("201")
        assert is_valid is False
        assert height is None

    def test_invalid_format(self):
        is_valid, height = is_valid_height("165cm")
        assert is_valid is False


class TestIsValidWeight:
    """Тесты для is_valid_weight."""

    def test_valid_weight_min(self):
        is_valid, weight = is_valid_weight("40")
        assert is_valid is True
        assert weight == 40

    def test_valid_weight_max(self):
        is_valid, weight = is_valid_weight("150")
        assert is_valid is True
        assert weight == 150

    def test_valid_weight_normal(self):
        is_valid, weight = is_valid_weight("55")
        assert is_valid is True
        assert weight == 55

    def test_invalid_too_light(self):
        is_valid, weight = is_valid_weight("39")
        assert is_valid is False
        assert weight is None

    def test_invalid_too_heavy(self):
        is_valid, weight = is_valid_weight("151")
        assert is_valid is False
        assert weight is None

    def test_invalid_format(self):
        is_valid, weight = is_valid_weight("55kg")
        assert is_valid is False


class TestIsValidCesarean:
    """Тесты для is_valid_cesarean."""

    def test_valid_zero(self):
        is_valid, cesarean, error = is_valid_cesarean("0")
        assert is_valid is True
        assert cesarean == 0
        assert error is None

    def test_valid_one(self):
        is_valid, cesarean, error = is_valid_cesarean("1")
        assert is_valid is True
        assert cesarean == 1
        assert error is None

    def test_invalid_two(self):
        is_valid, cesarean, error = is_valid_cesarean("2")
        assert is_valid is False
        assert cesarean == 2
        assert error == "too_many"

    def test_invalid_more(self):
        is_valid, cesarean, error = is_valid_cesarean("more")
        assert is_valid is False
        assert cesarean == "more"
        assert error == "too_many"

    def test_invalid_three(self):
        is_valid, cesarean, error = is_valid_cesarean("3")
        assert is_valid is False
        assert cesarean == 3
        assert error == "too_many"