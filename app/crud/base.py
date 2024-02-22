from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model) -> None:
        self.model = model

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value,
        session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        db_obj = await session.scalars(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.first()

    async def get_multi(
        self,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        model = self.model
        if user:
            db_objs = await session.scalars(
                select(model).where(model.user_id == user.id)
            )
            return db_objs.all()
        db_objs = await session.scalars(select(self.model))
        return db_objs.all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()

        if user:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj
