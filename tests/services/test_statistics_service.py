"""Тесты для StatisticsService."""
from datetime import datetime
from unittest.mock import patch

from services.statistics_service import StatisticsService


class TestCalculateAvgDuration:
    """Тесты для _calculate_avg_duration."""

    def test_returns_none_for_empty_list(self):
        result = StatisticsService._calculate_avg_duration([])
        assert result is None

    def test_returns_none_when_no_left_at(self):
        video_data = [
            {"joined_at": "2025-01-15T10:00:00Z", "left_at": None},
            {"joined_at": "2025-01-15T11:00:00Z", "left_at": None},
        ]
        result = StatisticsService._calculate_avg_duration(video_data)
        assert result is None

    def test_calculates_correct_average(self):
        video_data = [
            {"joined_at": "2025-01-15T10:00:00Z", "left_at": "2025-01-15T10:30:00Z"},  # 30 мин
            {"joined_at": "2025-01-15T11:00:00Z", "left_at": "2025-01-15T11:20:00Z"},  # 20 мин
        ]
        result = StatisticsService._calculate_avg_duration(video_data)
        assert result == 25  # (30 + 20) / 2

    def test_ignores_negative_duration(self):
        video_data = [
            {"joined_at": "2025-01-15T10:30:00Z", "left_at": "2025-01-15T10:00:00Z"},  # -30 мин (игнор)
            {"joined_at": "2025-01-15T11:00:00Z", "left_at": "2025-01-15T11:20:00Z"},  # 20 мин
        ]
        result = StatisticsService._calculate_avg_duration(video_data)
        assert result == 20

    def test_ignores_entries_without_left_at(self):
        video_data = [
            {"joined_at": "2025-01-15T10:00:00Z", "left_at": None},  # игнор
            {"joined_at": "2025-01-15T11:00:00Z", "left_at": "2025-01-15T11:30:00Z"},  # 30 мин
        ]
        result = StatisticsService._calculate_avg_duration(video_data)
        assert result == 30


class TestGetWeekRange:
    """Тесты для get_current_week_range и get_previous_week_range."""

    @patch("services.statistics_service.get_tashkent_now")
    def test_current_week_on_monday(self, mock_now):
        # Понедельник 13 января 2025
        mock_now.return_value = datetime(2025, 1, 13, 12, 0, 0)

        start, end = StatisticsService.get_current_week_range()

        assert start.day == 13
        assert start.month == 1
        assert start.hour == 0
        assert start.minute == 0
        assert end.day == 19
        assert end.hour == 23
        assert end.minute == 59

    @patch("services.statistics_service.get_tashkent_now")
    def test_current_week_on_sunday(self, mock_now):
        # Воскресенье 19 января 2025
        mock_now.return_value = datetime(2025, 1, 19, 12, 0, 0)

        start, end = StatisticsService.get_current_week_range()

        assert start.day == 13  # Понедельник
        assert end.day == 19  # Воскресенье

    @patch("services.statistics_service.get_tashkent_now")
    def test_previous_week(self, mock_now):
        # Понедельник 13 января 2025
        mock_now.return_value = datetime(2025, 1, 13, 12, 0, 0)

        start, end = StatisticsService.get_previous_week_range()

        assert start.day == 6  # Прошлый понедельник
        assert end.day == 12  # Прошлое воскресенье