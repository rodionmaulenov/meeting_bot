from supabase import AsyncClient

from models.application import Application


class ApplicationRepository:
    TABLE_NAME = "applications"
    SCHEMA = "meeting"

    def __init__(self, supabase: AsyncClient):
        self.supabase = supabase

    async def create(
        self,
        manager_id: int,
        member_id: int | None = None,
        full_name: str | None = None,
        telegram_phone: str | None = None,
        phones: list[str] | None = None,
        city: str | None = None,
        age: int | None = None,
        height: int | None = None,
        weight: int | None = None,
        children: str | int | None = None,
        cesarean: str | int | None = None,
        blood_type: str | None = None,
        status: str = "completed",
    ) -> Application:
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).insert({
            "manager_id": manager_id,
            "member_id": member_id,
            "full_name": full_name,
            "telegram_phone": telegram_phone,
            "phones": phones or [],
            "city": city,
            "age": age,
            "height": height,
            "weight": weight,
            "children": str(children) if children is not None else None,
            "cesarean": str(cesarean) if cesarean is not None else None,
            "blood_type": blood_type,
            "status": status,
        }).execute()

        return Application(**response.data[0])

    async def get_by_member_id(self, member_id: int) -> Application | None:
        response = await self.supabase.schema(self.SCHEMA).table(self.TABLE_NAME).select(
            "*"
        ).eq("member_id", member_id).execute()

        if not response.data:
            return None

        return Application(**response.data[0])