from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    APPROVED = "completed"    # Одобрена
    REJECTED = "rejected"    # Отклонена (возраст, кесарево, нет детей)


class Application(BaseModel):
    id: int
    member_id: int | None
    manager_id: int
    full_name: str | None
    telegram_phone: str | None
    phones: list[str]
    city: str | None
    age: int | None
    height: int | None
    weight: int | None
    children: str | None
    cesarean: str | None
    blood_type: str | None
    status: ApplicationStatus
    created_at: datetime