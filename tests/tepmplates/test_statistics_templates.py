"""Тесты для StatisticsTemplates."""
from datetime import datetime
from unittest.mock import patch

from services.statistics_service import ManagerStats, WeeklyStats
from templates import StatisticsTemplates


class TestFormatManager:
    """Тесты для _format_manager."""

    def test_full_data(self):
        manager = ManagerStats(
            manager_id=1,
            manager_name="Айнура",
            members_count=12,
            video_count=8,
            video_percent=67,
            avg_duration_minutes=24,
            completed_count=5,
            rejected_count=2,
        )

        result = StatisticsTemplates._format_manager(manager)

        assert "👤 Айнура" in result
        assert "Привела: 12" in result
        assert "Видео: 8 (67%)" in result
        assert "Ср. время: 24 мин" in result
        assert "✅ 5" in result
        assert "❌ 2" in result

    def test_no_video_data(self):
        manager = ManagerStats(
            manager_id=1,
            manager_name="Акмарал",
            members_count=5,
            video_count=0,
            video_percent=None,
            avg_duration_minutes=None,
            completed_count=0,
            rejected_count=0,
        )

        result = StatisticsTemplates._format_manager(manager)

        assert "Привела: 5" in result
        assert "Видео: —" in result
        assert "Ср. время: —" in result
        assert "Анкеты: —" in result


class TestFormatTotals:
    """Тесты для _format_totals."""

    def test_with_data(self):
        stats = WeeklyStats(
            start_date=datetime(2025, 1, 13),
            end_date=datetime(2025, 1, 19),
            managers=[],
            total_members=28,
            total_video=18,
            total_video_percent=64,
            total_completed=10,
            total_rejected=4,
        )

        result = StatisticsTemplates._format_totals(stats)

        assert "📈 Итого:" in result
        assert "Новых: 28" in result
        assert "Видео: 18 (64%)" in result
        assert "✅ 10" in result
        assert "❌ 4" in result

    def test_empty_data(self):
        stats = WeeklyStats(
            start_date=datetime(2025, 1, 13),
            end_date=datetime(2025, 1, 19),
            managers=[],
            total_members=0,
            total_video=0,
            total_video_percent=None,
            total_completed=0,
            total_rejected=0,
        )

        result = StatisticsTemplates._format_totals(stats)

        assert "Новых: 0" in result
        assert "Видео: —" in result
        assert "Анкеты: —" in result


class TestFormatFullStats:
    """Тесты для format_full_stats."""

    @patch("utils.time.get_tashkent_now")
    def test_contains_both_weeks(self, mock_now):
        mock_now.return_value = datetime(2025, 1, 15, 14, 35)

        current = WeeklyStats(
            start_date=datetime(2025, 1, 13),
            end_date=datetime(2025, 1, 19),
            managers=[],
            total_members=28,
            total_video=18,
            total_video_percent=64,
            total_completed=10,
            total_rejected=4,
        )

        previous = WeeklyStats(
            start_date=datetime(2025, 1, 6),
            end_date=datetime(2025, 1, 12),
            managers=[],
            total_members=23,
            total_video=15,
            total_video_percent=65,
            total_completed=9,
            total_rejected=3,
        )

        result = StatisticsTemplates.format_full_stats(current, previous)

        assert "Эта неделя (13.01 — 19.01)" in result
        assert "Прошлая неделя (06.01 — 12.01)" in result
        assert "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" in result
        assert "🕐 Обновлено: 15.01.2025 14:35" in result