import asyncio
from pyrogram import Client

from config import get_settings

settings = get_settings()


async def main():
    app = Client(
        name="user_session",
        api_id=settings.telegram_api_id,
        api_hash=settings.telegram_api_hash,
    )

    async with app:
        print("✅ Session created!")
        session_string = await app.export_session_string()
        print(f"\nДобавь в .env:")
        print(f"USER_SESSION_STRING={session_string}")


asyncio.run(main())