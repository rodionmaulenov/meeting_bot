from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    # Telegram
    bot_token: str
    bot_username: str
    telegram_api_id: int
    telegram_api_hash: str

    # Supabase
    supabase_url: str
    supabase_key: str

    # Группа команд (общая для всех проектов)
    commands_group_id: int
    commands_thread_id: int
    rules_message_id: int

    # Группа для девушек
    meeting_group_id: int
    announcement_message_id: int

    # Дашборд
    bot_type: str = "meeting_dashboard"
    redis_url: str
    user_session_string: str

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()