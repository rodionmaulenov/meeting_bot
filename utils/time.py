from datetime import datetime
from zoneinfo import ZoneInfo

TASHKENT_TZ = ZoneInfo("Asia/Tashkent")  # UTC+5


def get_tashkent_now() -> datetime:
    """Текущее время в Ташкенте."""
    return datetime.now(TASHKENT_TZ)


KYIV_TZ = ZoneInfo("Europe/Kyiv")  # UTC+2

def get_kyiv_now() -> datetime:
    """Текущее время в Киеве."""
    return datetime.now(KYIV_TZ)