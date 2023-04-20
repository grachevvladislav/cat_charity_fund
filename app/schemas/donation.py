from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationShortDB(DonationBase):
    id: int
    create_data: datetime

    class Config:
        orm_mode = True


class DonationFullDB(DonationShortDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime

    class Config(DonationBase.Config):
        pass
