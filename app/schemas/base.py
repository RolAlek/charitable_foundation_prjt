from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class BaseCreate(BaseModel):

    full_amount: PositiveInt


class CommonReadFields(BaseModel):

    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = Field(
        None,
        title='Дата закрытия',
        description='Устанавливается автоматически при закрытии'
    )
