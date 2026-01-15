"""Расписание периодических задач."""
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from workers.broker import broker
import workers.tasks  # noqa: F401

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)