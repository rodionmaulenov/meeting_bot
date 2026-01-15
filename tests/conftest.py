from pathlib import Path
from typing import Any, AsyncGenerator
from dotenv import load_dotenv

# =============================================================================
# ЗАГРУЗКА ТЕСТОВОГО ОКРУЖЕНИЯ
# =============================================================================
env_test_path = Path(__file__).parent.parent / ".env.test"
if env_test_path.exists():
    load_dotenv(env_test_path, override=True)

# Импортируем после загрузки .env
from config import get_settings

import pytest
from supabase import acreate_client, AsyncClient
from repositories.command_message_repository import CommandMessageRepository
from repositories.invite_link_repository import InviteLinkRepository
from repositories.member_repository import MemberRepository
from models.manager import Manager
from models.invite_link import InviteLink
from models.member import Member

# Фиксированные ID для тестов
TEST_MANAGER_TELEGRAM_ID = 999999999
TEST_MEMBER_TELEGRAM_ID = 888888888
TEST_INVITE_LINK = "https://t.me/+test_link_123"


@pytest.fixture
def settings():
    """Загрузить настройки из .env.test"""
    return get_settings()


@pytest.fixture
async def supabase(settings) -> AsyncClient:
    """Создать async клиент Supabase"""
    client = await acreate_client(
        settings.supabase_url,
        settings.supabase_key
    )
    return client


@pytest.fixture
async def command_message_repository(supabase, settings) -> AsyncGenerator[CommandMessageRepository, Any]:
    """Создать repository для тестов с автоочисткой"""
    repository = CommandMessageRepository(
        supabase=supabase,
        bot_type=settings.bot_type
    )

    yield repository

    await repository.delete_all_messages()


@pytest.fixture
async def test_manager(supabase: AsyncClient) -> AsyncGenerator[Manager, Any]:
    # Cleanup в правильном порядке (из-за foreign keys)
    await supabase.schema("meeting").table("video_chat_attendance").delete().neq(
        "id", 0
    ).execute()
    await supabase.schema("meeting").table("applications").delete().neq(
        "id", 0
    ).execute()  # ← ДОБАВЬ
    await supabase.schema("meeting").table("members").delete().eq(
        "telegram_id", TEST_MEMBER_TELEGRAM_ID
    ).execute()
    await supabase.schema("meeting").table("invite_links").delete().eq(
        "link", TEST_INVITE_LINK
    ).execute()
    await supabase.table("managers").delete().eq(
        "telegram_id", TEST_MANAGER_TELEGRAM_ID
    ).execute()

    response = await supabase.table("managers").insert({
        "telegram_id": TEST_MANAGER_TELEGRAM_ID,
        "name": "Test Manager",
        "is_active": True
    }).execute()

    manager = Manager(**response.data[0])
    yield manager

    # Cleanup после (тот же порядок)
    await supabase.schema("meeting").table("video_chat_attendance").delete().neq(
        "id", 0
    ).execute()
    await supabase.schema("meeting").table("applications").delete().neq(
        "id", 0
    ).execute()  # ← ДОБАВЬ
    await supabase.schema("meeting").table("members").delete().eq(
        "telegram_id", TEST_MEMBER_TELEGRAM_ID
    ).execute()
    await supabase.schema("meeting").table("invite_links").delete().eq(
        "link", TEST_INVITE_LINK
    ).execute()
    await supabase.table("managers").delete().eq("id", manager.id).execute()


@pytest.fixture
async def test_invite_link(
        supabase: AsyncClient,
        test_manager: Manager
) -> AsyncGenerator[InviteLink, Any]:
    """Тестовая invite-ссылка."""
    # Cleanup перед созданием
    await supabase.schema("meeting").table("video_chat_attendance").delete().neq(
        "id", 0
    ).execute()
    await supabase.schema("meeting").table("applications").delete().neq(
        "id", 0
    ).execute()  # ← ДОБАВЬ
    await supabase.schema("meeting").table("members").delete().eq(
        "telegram_id", TEST_MEMBER_TELEGRAM_ID
    ).execute()
    await supabase.schema("meeting").table("invite_links").delete().eq(
        "link", TEST_INVITE_LINK
    ).execute()

    # Создаём
    invite_link_repository = InviteLinkRepository(supabase=supabase)
    invite_link = await invite_link_repository.create(
        link=TEST_INVITE_LINK,
        manager_id=test_manager.id,
        member_name="Тестова Анна"
    )

    yield invite_link

    # Cleanup после
    await supabase.schema("meeting").table("video_chat_attendance").delete().neq(
        "id", 0
    ).execute()
    await supabase.schema("meeting").table("applications").delete().neq(
        "id", 0
    ).execute()  # ← ДОБАВЬ
    await supabase.schema("meeting").table("members").delete().eq(
        "telegram_id", TEST_MEMBER_TELEGRAM_ID
    ).execute()
    await supabase.schema("meeting").table("invite_links").delete().eq(
        "id", invite_link.id
    ).execute()


@pytest.fixture
async def test_member(
        supabase: AsyncClient,
        test_invite_link: InviteLink
) -> AsyncGenerator[Member, Any]:
    """Тестовая участница."""
    # Cleanup перед созданием
    await supabase.schema("meeting").table("video_chat_attendance").delete().neq(
        "id", 0
    ).execute()
    await supabase.schema("meeting").table("applications").delete().neq(
        "id", 0
    ).execute()  # ← ДОБАВЬ
    await supabase.schema("meeting").table("members").delete().eq(
        "telegram_id", TEST_MEMBER_TELEGRAM_ID
    ).execute()

    # Создаём
    member_repository = MemberRepository(supabase=supabase)
    member = await member_repository.create(
        telegram_id=TEST_MEMBER_TELEGRAM_ID,
        first_name="Анна",
        last_name="Тестова",
        username="anna_test",
        invite_link_id=test_invite_link.id
    )

    yield member

    # Cleanup после
    await supabase.schema("meeting").table("video_chat_attendance").delete().neq(
        "id", 0
    ).execute()
    await supabase.schema("meeting").table("applications").delete().neq(
        "id", 0
    ).execute()  # ← ДОБАВЬ
    await supabase.schema("meeting").table("members").delete().eq(
        "id", member.id
    ).execute()
