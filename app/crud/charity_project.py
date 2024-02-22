from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import ProjectUpdate
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def update_project(
        project: CharityProject,
        project_in: ProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        object_data = jsonable_encoder(project)
        update_data = project_in.dict(exclude_unset=True)
        if (
            update_data.get('full_amount') and
                (update_data['full_amount'] == object_data['invested_amount'])
        ):
            update_data['fully_invested'] = True
            update_data['close_date'] = datetime.now()

        for field in object_data:
            if field in update_data:
                setattr(project, field, update_data[field])

        session.add(project)
        await session.commit()
        await session.refresh(project)

        return project

    @staticmethod
    async def delete_project(
        project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(project)
        await session.commit()

        return project


charity_project_crud = CRUDCharityProject(CharityProject)