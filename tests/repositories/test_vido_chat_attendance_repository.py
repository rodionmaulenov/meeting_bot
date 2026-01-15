import pytest
from supabase import AsyncClient

from models.member import Member
from repositories.video_chat_attendance_repository import VideoChatAttendanceRepository
from utils.time import get_tashkent_now


class TestVideoChatAttendanceRepository:

    @pytest.fixture
    def repository(self, supabase: AsyncClient) -> VideoChatAttendanceRepository:
        return VideoChatAttendanceRepository(supabase=supabase)

    async def test_create_returns_attendance(
            self,
            repository: VideoChatAttendanceRepository,
            test_member: Member
    ):
        now = get_tashkent_now()
        today = now.date()

        attendance = await repository.create(
            member_id=test_member.id,
            meeting_date=today,
            joined_at=now
        )

        assert attendance.member_id == test_member.id
        assert attendance.meeting_date == today
        assert attendance.left_at is None

    async def test_update_left_at_updates_open_record(
            self,
            repository: VideoChatAttendanceRepository,
            test_member: Member,
            supabase: AsyncClient
    ):
        now = get_tashkent_now()
        today = now.date()

        # Создаём запись
        attendance = await repository.create(
            member_id=test_member.id,
            meeting_date=today,
            joined_at=now
        )
        assert attendance.left_at is None

        # Обновляем left_at
        await repository.update_left_at(
            member_id=test_member.id,
            meeting_date=today,
            left_at=now
        )

        # Проверяем
        response = await supabase.schema("meeting").table("video_chat_attendance").select(
            "*"
        ).eq("id", attendance.id).execute()

        assert response.data[0]["left_at"] is not None