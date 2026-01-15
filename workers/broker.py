"""Настройка Taskiq брокера."""
import logging
import colorlog
from aiogram import Bot

from pyrogram import Client
from redis.asyncio import from_url
from taskiq import TaskiqEvents, TaskiqState
from taskiq_redis import ListQueueBroker
from supabase import acreate_client

from config import get_settings

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_colors={
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }
))

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler],
    force=True
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("aiogram").setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
settings = get_settings()

broker = ListQueueBroker(url=settings.redis_url)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState):
    """Выполняется при старте worker'а."""

    # Redis
    state.redis = from_url(settings.redis_url)
    logger.info("Redis connected")

    # Supabase
    state.supabase = await acreate_client(
        settings.supabase_url,
        settings.supabase_key
    )
    logger.info("Supabase connected")

    # Userbot для Video Chat (user account)
    state.userbot = Client(
        name="userbot",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        session_string=settings.user_session_string,
    )
    await state.userbot.start()
    logger.info("Userbot connected")

    state.bot = Bot(token=settings.bot_token)
    logger.info("Bot connected")


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState):
    """Выполняется при остановке worker'а."""

    if hasattr(state, "userbot") and state.userbot:
        await state.userbot.stop()
        logger.info("Userbot disconnected")

    if hasattr(state, "redis") and state.redis:
        await state.redis.close()
        logger.info("Redis disconnected")

    if hasattr(state, "supabase") and state.supabase:
        await state.supabase.auth.sign_out()
        logger.info("Supabase disconnected")

    if hasattr(state, "bot") and state.bot:
        await state.bot.session.close()
        logger.info("bot disconnected")
