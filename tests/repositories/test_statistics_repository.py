"""Тесты для StatisticsRepository."""
import pytest
from datetime import datetime, timedelta

from repositories.statistics_repository import StatisticsRepository
from repositories.application_repository import ApplicationRepository
from models.manager import Manager
from models.member import Member


class TestStatisticsRepository:

    @pytest.fixture
    def statistics_repository(self, supabase) -> StatisticsRepository:
        return StatisticsRepository(supabase=supabase)

    @pytest.fixture
    def application_repository(self, supabase) -> ApplicationRepository:
        return ApplicationRepository(supabase=supabase)

    async def test_get_active_managers_returns_list(
        self,
        statistics_repository: StatisticsRepository,
        test_manager: Manager
    ):
        result = await statistics_repository.get_active_managers()

        assert isinstance(result, list)
        assert len(result) >= 1

        manager_ids = [m["id"] for m in result]
        assert test_manager.id in manager_ids

    async def test_get_members_by_manager_returns_members(
        self,
        statistics_repository: StatisticsRepository,
        test_manager: Manager,
        test_member: Member
    ):
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now() + timedelta(days=1)

        result = await statistics_repository.get_members_by_manager(
            manager_id=test_manager.id,
            start_date=start_date,
            end_date=end_date
        )

        assert isinstance(result, list)
        member_ids = [m["id"] for m in result]
        assert test_member.id in member_ids

    async def test_get_members_by_manager_empty_for_wrong_dates(
        self,
        statistics_repository: StatisticsRepository,
        test_manager: Manager,
        test_member: Member
    ):
        # Даты в прошлом — member не попадёт
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 1, 7)

        result = await statistics_repository.get_members_by_manager(
            manager_id=test_manager.id,
            start_date=start_date,
            end_date=end_date
        )

        assert result == []

    async def test_get_video_attendance_empty_for_no_members(
        self,
        statistics_repository: StatisticsRepository
    ):
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now() + timedelta(days=1)

        result = await statistics_repository.get_video_attendance_by_members(
            member_ids=[],
            start_date=start_date,
            end_date=end_date
        )

        assert result == []

    async def test_get_applications_count_by_status(
        self,
        statistics_repository: StatisticsRepository,
        application_repository: ApplicationRepository,
        test_manager: Manager,
        test_member: Member,
        supabase
    ):
        # Создаём анкету
        app = await application_repository.create(
            manager_id=test_manager.id,
            member_id=test_member.id,
            status="completed"
        )

        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)

        result = await statistics_repository.get_applications_count_by_status(
            manager_id=test_manager.id,
            status="completed",
            start_date=start_date,
            end_date=end_date
        )

        assert result >= 1

        # Cleanup
        await supabase.schema("meeting").table("applications").delete().eq(
            "id", app.id
        ).execute()

    async def test_get_applications_count_zero_for_wrong_status(
        self,
        statistics_repository: StatisticsRepository,
        application_repository: ApplicationRepository,
        test_manager: Manager,
        test_member: Member,
        supabase
    ):
        # Создаём completed анкету
        app = await application_repository.create(
            manager_id=test_manager.id,
            member_id=test_member.id,
            status="completed"
        )

        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)

        # Ищем rejected — должно быть 0
        result = await statistics_repository.get_applications_count_by_status(
            manager_id=test_manager.id,
            status="rejected",
            start_date=start_date,
            end_date=end_date
        )

        assert result == 0

        # Cleanup
        await supabase.schema("meeting").table("applications").delete().eq(
            "id", app.id
        ).execute()