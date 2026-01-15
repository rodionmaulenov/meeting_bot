"""Сервис для управления Video Chat через Pyrogram."""
import json
import logging
import random
from datetime import datetime

from pyrogram import Client
from pyrogram.raw.functions.phone import CreateGroupCall
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class VideoChatService:
    """Сервис для создания и управления Video Chat."""

    REDIS_KEY = "meeting_bot:video_chat"
    REDIS_TTL = 172800  # 48 часов

    def __init__(self, client: Client, redis: Redis, group_id: int):
        self.client = client
        self.redis = redis
        self.group_id = group_id

    async def schedule_video_chat(
            self,
            schedule_date: datetime,
            title: str = "Еженедельная встреча"
    ) -> str | None:
        """Запланировать Video Chat."""
        try:
            peer = await self.client.resolve_peer(self.group_id)

            result = await self.client.invoke(
                CreateGroupCall(
                    peer=peer,
                    random_id=random.randint(1, 2147483647),
                    title=title,
                    schedule_date=int(schedule_date.timestamp()),
                )
            )

            group_call = None
            for update in result.updates:
                if hasattr(update, 'call'):
                    group_call = update.call
                    break

            if not group_call:
                logger.error("Could not find group_call in response")
                return None

            # Для приватных групп используем ID группы
            # Участницы увидят scheduled video chat в группе
            link = f"https://t.me/c/{str(self.group_id).replace('-100', '')}"

            data = {
                "call_id": group_call.id,
                "access_hash": group_call.access_hash,
                "link": link,
                "title": title,
                "scheduled_for": schedule_date.isoformat()
            }
            await self.redis.set(
                self.REDIS_KEY,
                json.dumps(data),
                ex=self.REDIS_TTL
            )

            logger.debug(f"Scheduled video chat '{title}' for {schedule_date}")
            logger.debug(f"Group link: {link}")

            return link

        except Exception as e:
            logger.error(f"Failed to schedule video chat: {e}")
            return None