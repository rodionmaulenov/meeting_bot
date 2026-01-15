import pytest

from models.manager import Manager
from repositories.manager_repository import ManagerRepository


class TestManagerRepository:

    @pytest.fixture
    def manager_repository(self, supabase) -> ManagerRepository:
        return ManagerRepository(supabase=supabase)

    async def test_get_by_telegram_id_returns_manager_when_exists(
            self,
            manager_repository: ManagerRepository,
            test_manager: Manager  # ← из conftest.py
    ):
        result = await manager_repository.get_by_telegram_id(test_manager.telegram_id)

        assert result is not None
        assert result.id == test_manager.id
        assert result.telegram_id == test_manager.telegram_id

    async def test_get_by_telegram_id_returns_none_when_not_exists(
            self,
            manager_repository: ManagerRepository
    ):
        result = await manager_repository.get_by_telegram_id(111111111)
        assert result is None