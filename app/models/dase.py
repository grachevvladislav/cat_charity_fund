import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class CharityDonationBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    create_date = Column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
    close_date = Column(DateTime, default=None)
