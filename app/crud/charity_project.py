from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import ProjectUpdate
from app.crud.base import CRUDBase


SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTES = 60


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

    @staticmethod
    async def get_projects_by_completion_rate(session: AsyncSession):
        projects = await session.execute(
            select([
                CharityProject.name,
                CharityProject.create_date,
                CharityProject.close_date,
                CharityProject.description
            ]).where(
                CharityProject.fully_invested.is_(True)
            )
        )

        projects = [
            {
                'name': project[0],
                'duration': project[2] - project[1],
                'description': project[3]
            } for project in projects
        ]
        projects = sorted(projects, key=lambda project: project['duration'])

        for project in projects:
            duration = project['duration']
            days = duration.days
            hours, remainder = divmod(duration.seconds, SECONDS_IN_HOUR)
            minutes, seconds = divmod(remainder, SECONDS_IN_MINUTES)
            formated_duration = '{0} {1}, {2:02}:{3:02}:{4:02}.{5:06}'.format(
                days, 'day' if days == 1 else 'days', hours, minutes, seconds,
                duration.microseconds // 1000
            )
            project['duration'] = formated_duration

        return projects


charity_project_crud = CRUDCharityProject(CharityProject)