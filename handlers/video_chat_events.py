"""Handler для отслеживания участников Video Chat."""
import json
import logging

from pyrogram import ContinuePropagation
from pyrogram.raw.types import (
    UpdateGroupCallParticipants,
)
from redis.asyncio import Redis

from repositories.member_repository import MemberRepository
from repositories.video_chat_attendance_repository import VideoChatAttendanceRepository
from services.video_chat_service import VideoChatService
from utils.time import get_tashkent_now

logger = logging.getLogger(__name__)


async def on_video_chat_participant(
        update: UpdateGroupCallParticipants,
        redis: Redis,
        member_repository: MemberRepository,
        attendance_repository: VideoChatAttendanceRepository
) -> None:
    """Обработка событий join/left в Video Chat."""

    # DEBUG: Логируем ВСЕ raw updates
    logger.info(f"Raw update received: {type(update).__name__}")

    # 1. Это нужный тип события?
    if not isinstance(update, UpdateGroupCallParticipants):
        raise ContinuePropagation

    logger.info(f"Video chat event: {update}")

    # 2. Есть активный Video Chat в Redis?
    video_chat_data = await redis.get(VideoChatService.REDIS_KEY)
    if not video_chat_data:
        raise ContinuePropagation

    # 3. Это наш Video Chat?
    parsed = json.loads(video_chat_data)
    if update.call.id != parsed.get("call_id"):  # type: ignore[union-attr]
        raise ContinuePropagation

    # 4. Обрабатываем каждого участника
    now = get_tashkent_now()
    today = now.date()

    for participant in update.participants:  # type: ignore[union-attr]
        # Получаем telegram_id из peer
        telegram_id = participant.peer.user_id  # type: ignore[union-attr]

        # Ищем member в БД
        member = await member_repository.get_by_telegram_id(telegram_id)
        if not member:
            # Не наша участница (возможно админ) — игнорируем
            logger.debug(f"Unknown user {telegram_id}, skipping")
            continue

        # Join
        if participant.just_joined:  # type: ignore[union-attr]
            await attendance_repository.create(
                member_id=member.id,
                meeting_date=today,
                joined_at=now
            )
            logger.debug(f"Member {member.id} joined video chat")

        # Left
        elif participant.left:  # type: ignore[union-attr]
            await attendance_repository.update_left_at(
                member_id=member.id,
                meeting_date=today,
                left_at=now
            )
            logger.debug(f"Member {member.id} left video chat")

    raise ContinuePropagation