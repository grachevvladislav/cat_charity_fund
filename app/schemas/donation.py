from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationUpdate(DonationBase):
    full_amount: PositiveInt
    comment: Optional[str]
    fully_invested: Optional[bool]
    invested_amount: Optional[PositiveInt]
    close_date: Optional[datetime]


class DonationCreateDB(DonationBase):
    id: int
    create_date: datetime
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        orm_mode = True


class DonationListDB(DonationCreateDB):
    user_id: int
    fully_invested: bool
    close_date: Optional[datetime]
    invested_amount: int
    comment: Optional[str]


class DonationMyListDB(DonationCreateDB):
    close_date: Optional[datetime]
    comment: Optional[str]


class DonationFullDB(DonationCreateDB):
    user_id: int
    fully_invested: bool
    close_date: Optional[datetime]
    invested_amount: int
    comment: Optional[str]
