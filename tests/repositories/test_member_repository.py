import pytest

from models.invite_link import InviteLink
from models.member import Member
from repositories.member_repository import MemberRepository


class TestMemberRepository:

    @pytest.fixture
    def member_repository(self, supabase) -> MemberRepository:
        return MemberRepository(supabase=supabase)

    async def test_create_returns_member(
            self,
            member_repository: MemberRepository,
            test_invite_link: InviteLink,
            supabase
    ):
        test_telegram_id = 123456789

        # Cleanup перед
        await supabase.schema("meeting").table("members").delete().eq(
            "telegram_id", test_telegram_id
        ).execute()

        result = await member_repository.create(
            telegram_id=test_telegram_id,
            first_name="Анна",
            last_name="Тестова",
            username="anna_testova",
            invite_link_id=test_invite_link.id
        )

        assert result.telegram_id == test_telegram_id
        assert result.first_name == "Анна"
        assert result.last_name == "Тестова"
        assert result.username == "anna_testova"
        assert result.invite_link_id == test_invite_link.id

        # Cleanup после
        await supabase.schema("meeting").table("members").delete().eq(
            "id", result.id
        ).execute()

    async def test_get_all_returns_members(
            self,
            member_repository: MemberRepository,
            test_invite_link: InviteLink,
            supabase
    ):
        telegram_id_1 = 111111111
        telegram_id_2 = 222222222

        # Cleanup перед
        await supabase.schema("meeting").table("members").delete().eq(
            "telegram_id", telegram_id_1
        ).execute()
        await supabase.schema("meeting").table("members").delete().eq(
            "telegram_id", telegram_id_2
        ).execute()

        # Создаём двух участниц
        member1 = await member_repository.create(
            telegram_id=telegram_id_1,
            first_name="Айгуль",
            last_name="Каримова",
            username="aigul",
            invite_link_id=test_invite_link.id
        )
        member2 = await member_repository.create(
            telegram_id=telegram_id_2,
            first_name="Мадина",
            last_name="Ахметова",
            username=None,
            invite_link_id=test_invite_link.id
        )

        # Вызываем метод
        result = await member_repository.get_all()

        # Проверяем
        assert len(result) >= 2
        telegram_ids = [m.telegram_id for m in result]
        assert telegram_id_1 in telegram_ids
        assert telegram_id_2 in telegram_ids

        # Cleanup после
        await supabase.schema("meeting").table("members").delete().eq("id", member1.id).execute()
        await supabase.schema("meeting").table("members").delete().eq("id", member2.id).execute()

    async def test_get_by_telegram_id_returns_member(
            self,
            member_repository: MemberRepository,
            test_member: Member
    ):
        result = await member_repository.get_by_telegram_id(test_member.telegram_id)

        assert result is not None
        assert result.id == test_member.id

    async def test_get_by_telegram_id_returns_none_when_not_found(
            self,
            member_repository: MemberRepository
    ):
        result = await member_repository.get_by_telegram_id(999999999)

        assert result is None
