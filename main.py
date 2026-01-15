import asyncio
import logging
import colorlog
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from supabase import acreate_client, AsyncClient
from pyrogram import Client
from redis.asyncio import from_url as redis_from_url

from middlewares.commands import CommandsMiddleware
from repositories.video_chat_attendance_repository import VideoChatAttendanceRepository
from handlers.video_chat_events import on_video_chat_participant
from config import get_settings
from repositories.command_message_repository import CommandMessageRepository
from repositories.invite_link_repository import InviteLinkRepository
from repositories.manager_repository import ManagerRepository
from services.command_message_service import CommandMessageService
from repositories.member_repository import MemberRepository
from repositories.application_repository import ApplicationRepository
from handlers.application import router as application_router
from handlers.member_joined import router as member_joined_router
from handlers.clear import router as clear_router
from handlers.add import router as add_router
from handlers.service_messages import router as service_messages_router
from services.invite_link_service import InviteLinkService

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


@asynccontextmanager
async def lifespan(settings):
    logger.info("Starting bot...")

    supabase: AsyncClient = await acreate_client(
        settings.supabase_url,
        settings.supabase_key
    )
    bot = Bot(token=settings.bot_token)
    redis = redis_from_url(settings.redis_url)

    # Userbot для прослушивания Video Chat событий
    userbot = Client(
        name="meeting_bot_userbot",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        session_string=settings.user_session_string,
        no_updates=False  # Важно! Нужны updates
    )

    logger.info("Supabase, Bot, Redis, Userbot initialized")

    yield {"supabase": supabase, "bot": bot, "redis": redis, "userbot": userbot}

    logger.info("Shutting down...")
    await bot.session.close()
    await redis.close()
    await supabase.auth.sign_out()


async def main():
    settings = get_settings()

    async with lifespan(settings) as resources:
        supabase = resources["supabase"]
        bot = resources["bot"]
        redis = resources["redis"]
        userbot = resources["userbot"]

        dp = Dispatcher()

        # 1. Создаём repository
        command_message_repository = CommandMessageRepository(
            supabase=supabase,
            bot_type=settings.bot_type
        )
        invite_link_repository = InviteLinkRepository(
            supabase=supabase,
        )
        manager_repository = ManagerRepository(
            supabase=supabase,
        )
        member_repository = MemberRepository(
            supabase=supabase,
        )
        video_chat_attendance_repository = VideoChatAttendanceRepository(
            supabase=supabase
        )
        application_repository = ApplicationRepository(
            supabase=supabase
        )

        # 2. Создаём service
        command_message_service = CommandMessageService(
            bot=bot,
            repository=command_message_repository,
            chat_id=settings.commands_group_id
        )
        invite_link_service = InviteLinkService(
            bot=bot,
            manager_repository=manager_repository,
            invite_link_repository=invite_link_repository,
            group_id=settings.meeting_group_id
        )

        # Регистрируем handler для Video Chat событий
        @userbot.on_raw_update()
        async def video_chat_handler(client, update, users, chats):
            logger.debug(f"RAW UPDATE: {type(update).__name__}")
            await on_video_chat_participant(
                update=update,
                redis=redis,
                member_repository=member_repository,
                attendance_repository=video_chat_attendance_repository
            )

        # 3. Передаём в dispatcher
        dp["command_message_service"] = command_message_service
        dp["invite_link_service"] = invite_link_service
        dp["member_repository"] = member_repository
        dp["application_repository"] = application_repository
        dp["invite_link_repository"] = invite_link_repository

        # 4. Подключаем middleware
        dp.message.outer_middleware(CommandsMiddleware(
            manager_repository=manager_repository,
            command_message_repository=command_message_repository
        ))

        # 5. Подключаем router
        dp.include_router(service_messages_router)
        dp.include_router(clear_router)
        dp.include_router(add_router)
        dp.include_router(member_joined_router)
        dp.include_router(application_router)

        # 6. Запускаем polling
        logger.info("Bot is running. Press Ctrl+C to stop.")
        await userbot.start()
        try:
            await dp.start_polling(bot, allowed_updates=["message", "chat_member", "callback_query"])
        finally:
            await userbot.stop()


if __name__ == "__main__":
    asyncio.run(main())
