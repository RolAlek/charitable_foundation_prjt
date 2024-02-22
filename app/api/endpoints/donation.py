from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.core.db import get_async_session
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationSuperuserDB,
)
from app.models import User
from app.core.user import current_user, current_superuser
from app.utils import investing


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation_in, session, user)
    return await investing(new_donation, session)


@router.get(
    '/',
    response_model=list[DonationSuperuserDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Получает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationDB])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список моих пожертвований."""
    return await donation_crud.get_multi(session, user)