from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_objects(model, session: AsyncSession):
    objects = await session.scalars(
        select(model)
        .where(model.fully_invested.is_(False))
        .order_by(model.create_date)
    )
    return objects


async def investing(
    requesting_obj, session: AsyncSession
):

    model = (
        Donation if isinstance(requesting_obj, CharityProject)
        else CharityProject
    )
    objects = await get_objects(model, session)

    if not objects:
        return requesting_obj

    for providing_obj in objects:
        available_funds = (
            requesting_obj.full_amount - requesting_obj.invested_amount
        )
        required_investments = (
            providing_obj.full_amount - providing_obj.invested_amount
        )

        if available_funds > required_investments:
            providing_obj.invested_amount = (
                providing_obj.invested_amount + required_investments
            )
            requesting_obj.invested_amount += required_investments
        else:
            providing_obj.invested_amount = (
                providing_obj.invested_amount + available_funds
            )
            requesting_obj.invested_amount += available_funds

        providing_obj.fully_invested = (
            providing_obj.full_amount == providing_obj.invested_amount
        )

        if providing_obj.fully_invested:
            providing_obj.close_date = datetime.now()

        requesting_obj.fully_invested = (
            requesting_obj.full_amount == requesting_obj.invested_amount
        )

        if requesting_obj.fully_invested:
            requesting_obj.close_date = datetime.now()

        session.add(providing_obj)

    session.add(requesting_obj)
    await session.commit()
    await session.refresh(requesting_obj)
    return requesting_obj