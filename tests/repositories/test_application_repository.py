"""Тесты для ApplicationRepository."""
import pytest

from models.manager import Manager
from models.member import Member
from repositories.application_repository import ApplicationRepository


class TestApplicationRepository:

    @pytest.fixture
    def application_repository(self, supabase) -> ApplicationRepository:
        return ApplicationRepository(supabase=supabase)

    async def test_create_returns_application(
            self,
            application_repository: ApplicationRepository,
            test_manager: Manager,
            test_member: Member,
            supabase
    ):
        result = await application_repository.create(
            manager_id=test_manager.id,
            member_id=test_member.id,
            full_name="Karimova Malika Rustamovna",
            telegram_phone="+998901234567",
            phones=["+998901234567"],
            city="Ташкентская",
            age=25,
            height=165,
            weight=55,
            children=2,
            cesarean=0,
            blood_type="II+",
            status="completed",
        )

        assert result.id is not None
        assert result.manager_id == test_manager.id
        assert result.member_id == test_member.id
        assert result.full_name == "Karimova Malika Rustamovna"
        assert result.telegram_phone == "+998901234567"
        assert result.phones == ["+998901234567"]
        assert result.city == "Ташкентская"
        assert result.age == 25
        assert result.height == 165
        assert result.weight == 55
        assert result.children == "2"
        assert result.cesarean == "0"
        assert result.blood_type == "II+"
        assert result.status == "completed"

        # Cleanup
        await supabase.schema("meeting").table("applications").delete().eq(
            "id", result.id
        ).execute()

    async def test_create_rejected_with_partial_data(
            self,
            application_repository: ApplicationRepository,
            test_manager: Manager,
            test_member: Member,
            supabase
    ):
        """Тест создания rejected анкеты с частичными данными."""
        result = await application_repository.create(
            manager_id=test_manager.id,
            member_id=test_member.id,
            telegram_phone="+998901234567",
            phones=["+998901234567"],
            age=45,
            status="rejected",
        )

        assert result.id is not None
        assert result.status == "rejected"
        assert result.age == 45
        assert result.full_name is None
        assert result.city is None

        # Cleanup
        await supabase.schema("meeting").table("applications").delete().eq(
            "id", result.id
        ).execute()

    async def test_get_by_member_id_returns_application_when_exists(
            self,
            application_repository: ApplicationRepository,
            test_manager: Manager,
            test_member: Member,
            supabase
    ):
        # Создаём анкету
        created = await application_repository.create(
            manager_id=test_manager.id,
            member_id=test_member.id,
            full_name="Test User",
            status="completed",
        )

        result = await application_repository.get_by_member_id(test_member.id)

        assert result is not None
        assert result.id == created.id
        assert result.member_id == test_member.id

        # Cleanup
        await supabase.schema("meeting").table("applications").delete().eq(
            "id", created.id
        ).execute()

    async def test_get_by_member_id_returns_none_when_not_exists(
            self,
            application_repository: ApplicationRepository
    ):
        result = await application_repository.get_by_member_id(999999)

        assert result is None

    async def test_children_and_cesarean_stored_as_string(
            self,
            application_repository: ApplicationRepository,
            test_manager: Manager,
            test_member: Member,
            supabase
    ):
        """Тест что children и cesarean конвертируются в строки."""
        result = await application_repository.create(
            manager_id=test_manager.id,
            member_id=test_member.id,
            children="more",
            cesarean=1,
            status="completed",
        )

        assert result.children == "more"
        assert result.cesarean == "1"

        # Cleanup
        await supabase.schema("meeting").table("applications").delete().eq(
            "id", result.id
        ).execute()