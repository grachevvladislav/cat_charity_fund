from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]
    fully_invested: Optional[bool]
    invested_amount: Optional[PositiveInt]
    close_date: Optional[datetime]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: int
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
