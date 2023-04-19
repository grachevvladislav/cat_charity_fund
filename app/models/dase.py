import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class CharityDonationBase(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    close_date = Column(DateTime, default=None)
