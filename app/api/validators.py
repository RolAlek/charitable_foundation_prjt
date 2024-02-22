from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_duplicate_project_name(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_exists = await charity_project_crud.get_by_attribute(
        'name', project_name, session
    )
    if project_exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_before_update(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )

    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект с таким id не найден.',
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    return project


async def cant_lt(
    project: CharityProject,
    amount_value: int,
) -> None:
    if amount_value < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Сумма должана быть не меньше уже вложенной!'
        )


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project
