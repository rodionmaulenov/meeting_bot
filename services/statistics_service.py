"""Сервис статистики."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from repositories.statistics_repository import StatisticsRepository
from utils.time import get_tashkent_now


@dataclass
class ManagerStats:
    """Статистика по менеджеру."""
    manager_id: int
    manager_name: str
    members_count: int
    video_count: int
    video_percent: int | None
    avg_duration_minutes: int | None
    completed_count: int
    rejected_count: int


@dataclass
class WeeklyStats:
    """Статистика за неделю."""
    start_date: datetime
    end_date: datetime
    managers: list[ManagerStats]
    total_members: int
    total_video: int
    total_video_percent: int | None
    total_completed: int
    total_rejected: int


class StatisticsService:
    """Сервис для сбора и расчёта статистики."""

    def __init__(self, repository: StatisticsRepository):
        self.repository = repository

    async def get_weekly_stats(
            self,
            start_date: datetime,
            end_date: datetime
    ) -> WeeklyStats:
        """Получить статистику за период."""
        managers = await self.repository.get_active_managers()

        managers_stats = []
        for manager in managers:
            stats = await self._get_manager_stats(
                manager_id=manager["id"],
                manager_name=manager["name"],
                start_date=start_date,
                end_date=end_date
            )
            managers_stats.append(stats)

        # Итого
        total_members = sum(m.members_count for m in managers_stats)
        total_video = sum(m.video_count for m in managers_stats)
        total_completed = sum(m.completed_count for m in managers_stats)
        total_rejected = sum(m.rejected_count for m in managers_stats)

        total_video_percent = None
        if total_members > 0:
            total_video_percent = round(total_video / total_members * 100)

        return WeeklyStats(
            start_date=start_date,
            end_date=end_date,
            managers=managers_stats,
            total_members=total_members,
            total_video=total_video,
            total_video_percent=total_video_percent,
            total_completed=total_completed,
            total_rejected=total_rejected,
        )

    async def _get_manager_stats(
            self,
            manager_id: int,
            manager_name: str,
            start_date: datetime,
            end_date: datetime
    ) -> ManagerStats:
        """Статистика по одному менеджеру."""
        # 1. Привела
        members = await self.repository.get_members_by_manager(
            manager_id, start_date, end_date
        )
        members_count = len(members)
        member_ids = [m["id"] for m in members]

        # 2. На видео + среднее время
        video_data = await self.repository.get_video_attendance_by_members(
            member_ids, start_date, end_date
        )

        video_count = len(set(v["member_id"] for v in video_data))
        avg_duration_minutes = self._calculate_avg_duration(video_data)

        # 3. Процент
        video_percent = None
        if members_count > 0:
            video_percent = round(video_count / members_count * 100)

        # 4. Анкеты
        completed_count = await self.repository.get_applications_count_by_status(
            manager_id, "completed", start_date, end_date
        )
        rejected_count = await self.repository.get_applications_count_by_status(
            manager_id, "rejected", start_date, end_date
        )

        return ManagerStats(
            manager_id=manager_id,
            manager_name=manager_name,
            members_count=members_count,
            video_count=video_count,
            video_percent=video_percent,
            avg_duration_minutes=avg_duration_minutes,
            completed_count=completed_count,
            rejected_count=rejected_count,
        )

    @staticmethod
    def _calculate_avg_duration(video_data: list[dict]) -> int | None:
        """Рассчитать среднее время на видео."""
        durations = []

        for v in video_data:
            if v["left_at"] and v["joined_at"]:
                joined = datetime.fromisoformat(
                    v["joined_at"].replace("Z", "+00:00")
                )
                left = datetime.fromisoformat(
                    v["left_at"].replace("Z", "+00:00")
                )
                duration = (left - joined).total_seconds() / 60
                if duration > 0:
                    durations.append(duration)

        if not durations:
            return None

        return round(sum(durations) / len(durations))

    @staticmethod
    def get_current_week_range() -> tuple[datetime, datetime]:
        """Диапазон текущей недели (Пн-Вс)."""
        now = get_tashkent_now()
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start, end

    @staticmethod
    def get_previous_week_range() -> tuple[datetime, datetime]:
        """Диапазон прошлой недели (Пн-Вс)."""
        now = get_tashkent_now()
        start = now - timedelta(days=now.weekday() + 7)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start, end
