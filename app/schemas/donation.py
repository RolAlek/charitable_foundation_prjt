from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.base import BaseCreate, CommonReadFields


class DonationCreate(BaseCreate):

    comment: Optional[str] = Field(
        None,
        min_length=1,
        title='Коментарий',
        description='По желанию жертвователя'
    )


class DonationDB(DonationCreate):

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperuserDB(DonationDB, CommonReadFields):

    user_id: int

    class Config:
        orm_mode = True
