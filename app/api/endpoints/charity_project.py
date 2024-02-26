from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.core.db import get_async_session
from app.schemas.charity_project import ProjectDB, ProjectCreate, ProjectUpdate
from app.api.validators import (
    check_duplicate_project_name,
    check_project_before_update,
    check_project_before_delete,
    cant_lt,
)
from app.core.user import current_superuser
from app.services.utils import investing


router = APIRouter()


@router.get(
    '/',
    response_model=list[ProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех благотварительных проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    path='/',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project_in: ProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Создает благотворительный проект.
    """
    await check_duplicate_project_name(project_in.name, session)
    new_project = await charity_project_crud.create(project_in, session)
    return await investing(new_project, session)


@router.delete(
    path='/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
     средства, его можно только закрыть.
    """
    project = await check_project_before_delete(project_id, session)
    return await charity_project_crud.delete_project(project, session)


@router.patch(
    path='/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project_in: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать, также нельзя установить требуемую
     сумму меньше уже вложенной.
    """
    project = await check_project_before_update(project_id, session)

    if project_in.name:
        await check_duplicate_project_name(project_in.name, session)
    if project_in.full_amount:
        await cant_lt(project, project_in.full_amount)

    return await charity_project_crud.update_project(
        project, project_in, session
    )
