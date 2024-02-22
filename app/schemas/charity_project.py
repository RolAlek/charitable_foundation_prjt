from datetime import datetime
from typing import Optional

from pydantic import Extra, Field, PositiveInt, validator

from app.schemas.base import BaseCreate, CommonReadFields


class ProjectCreate(BaseCreate):

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Название',
        description='Обязательно для запоолнения'
    )
    description: str = Field(
        ...,
        min_length=1,
        title='Описание',
        description='Обязательно для запоолнения'
    )


class ProjectUpdate(ProjectCreate):

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        title='Название',
        description='Опционально'
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        title='Описание',
        description='Опционально'
    )
    full_amount: Optional[PositiveInt]

    class Config:

        extra = Extra.forbid

    @validator('name', 'description')
    def colums_cant_be_null(cls, value):
        if value is None:
            raise ValueError(
                'Название проекта или его описание не могут быт пустыми.'
            )
        return value


class ProjectDB(ProjectCreate, CommonReadFields):

    create_date: datetime = Field(
        ...,
        title='Дата создания',
        description=('Устанавливается автоматически при создании'
                     ' благотварительного проекта')
    )
    id: int

    class Config:
        orm_mode = True
