"""Импорт всех задач для регистрации."""
from workers.tasks.schedule_video_chat import schedule_video_chat  # noqa: F401
from workers.tasks.update_meeting_announcement import (  # noqa: F401
    update_meeting_announcement,
    final_meeting_reminder,
)
from workers.tasks.cleanup_group import cleanup_group  # noqa: F401
from workers.tasks.send_application_button import send_application_button  # noqa: F401
from workers.tasks.update_statistics import update_statistics # noqa: F401