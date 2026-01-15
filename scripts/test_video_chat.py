import asyncio
from datetime import datetime, timedelta

from pyrogram import Client
from redis.asyncio import from_url

from config import get_settings
from services.video_chat_service import VideoChatService

settings = get_settings()


async def main():
    # Инициализация
    userbot = Client(
        name="test_video_chat",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
        session_string=settings.user_session_string,
    )
    redis = from_url(settings.redis_url)

    async with userbot:
        service = VideoChatService(
            client=userbot,
            redis=redis,
            group_id=settings.meeting_group_id
        )

        # Создаём Video Chat через 2 минуты
        schedule_date = datetime.now() + timedelta(minutes=5)
        result = await service.schedule_video_chat(schedule_date=schedule_date)
        print(f"Video Chat создан: {result}")

        # Проверяем Redis
        data = await redis.get(VideoChatService.REDIS_KEY)
        print(f"Redis data: {data}")

    await redis.close()


if __name__ == "__main__":
    asyncio.run(main())