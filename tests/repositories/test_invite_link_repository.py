import pytest
from supabase import AsyncClient

from models.manager import Manager
from models.invite_link import InviteLink
from repositories.invite_link_repository import InviteLinkRepository


class TestInviteLinkRepository:

    @pytest.fixture
    def invite_link_repository(self, supabase) -> InviteLinkRepository:
        return InviteLinkRepository(supabase=supabase)

    async def test_create_returns_invite_link(
            self,
            invite_link_repository: InviteLinkRepository,
            test_manager: Manager,
            supabase
    ):
        test_link = "https://t.me/+xyz789test"

        # Cleanup перед
        await supabase.schema("meeting").table("invite_links").delete().eq(
            "link", test_link
        ).execute()

        result = await invite_link_repository.create(
            link=test_link,
            manager_id=test_manager.id,
            member_name="Иванова Мария"
        )

        assert result.link == test_link
        assert result.manager_id == test_manager.id
        assert result.member_name == "Иванова Мария"
        assert result.is_used is False

        # Cleanup после
        await supabase.schema("meeting").table("invite_links").delete().eq(
            "id", result.id
        ).execute()

    async def test_get_by_link_returns_invite_link_when_exists(
            self,
            invite_link_repository: InviteLinkRepository,
            test_invite_link: InviteLink
    ):
        result = await invite_link_repository.get_by_link(test_invite_link.link)

        assert result is not None
        assert result.id == test_invite_link.id
        assert result.link == test_invite_link.link

    async def test_get_by_link_returns_none_when_not_exists(
            self,
            invite_link_repository: InviteLinkRepository
    ):
        result = await invite_link_repository.get_by_link("https://t.me/+nonexistent")

        assert result is None

    async def test_mark_as_used_updates_is_used(
            self,
            invite_link_repository: InviteLinkRepository,
            test_invite_link: InviteLink
    ):
        assert test_invite_link.is_used is False

        await invite_link_repository.mark_as_used(test_invite_link.id)

        result = await invite_link_repository.get_by_link(test_invite_link.link)
        assert result is not None
        assert result.is_used is True

    async def test_delete_unused_removes_only_unused_links(
            self,
            invite_link_repository: InviteLinkRepository,
            test_manager: Manager,
            supabase: AsyncClient
    ):
        # Создаём 2 ссылки
        await invite_link_repository.create(
            link="https://t.me/+unused_link",
            manager_id=test_manager.id,
            member_name="Unused"
        )
        link2 = await invite_link_repository.create(
            link="https://t.me/+used_link",
            manager_id=test_manager.id,
            member_name="Used"
        )

        # Помечаем одну как использованную
        await invite_link_repository.mark_as_used(link2.id)

        # Удаляем неиспользованные
        deleted_count = await invite_link_repository.delete_unused()

        # Проверяем
        assert deleted_count == 1
        assert await invite_link_repository.get_by_link("https://t.me/+unused_link") is None
        assert await invite_link_repository.get_by_link("https://t.me/+used_link") is not None

        # Cleanup
        await supabase.schema("meeting").table("invite_links").delete().eq(
            "id", link2.id
        ).execute()

    async def test_get_by_id_returns_invite_link_when_exists(
            self,
            invite_link_repository: InviteLinkRepository,
            test_invite_link: InviteLink
    ):
        result = await invite_link_repository.get_by_id(test_invite_link.id)

        assert result is not None
        assert result.id == test_invite_link.id
        assert result.link == test_invite_link.link

    async def test_get_by_id_returns_none_when_not_exists(
            self,
            invite_link_repository: InviteLinkRepository
    ):
        result = await invite_link_repository.get_by_id(999999)

        assert result is None