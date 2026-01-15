import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile
from config import get_settings

settings = get_settings()


async def main():
    bot = Bot(token=settings.bot_token)

    # Отправляем фото с подписью
    photo = FSInputFile("assets/notify_screenshot.jpg")

    msg = await bot.send_photo(
        chat_id=settings.meeting_group_id,
        photo=photo,
        caption="📢 Объявление о встрече",
        parse_mode="HTML"
    )

    print(f"✅ Message ID: {msg.message_id}")
    print(f"Добавь в .env: ANNOUNCEMENT_MESSAGE_ID={msg.message_id}")

    await bot.session.close()


asyncio.run(main())