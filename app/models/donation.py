import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text, Integer

from .dase import CharityDonationBase


class Donation(CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    close_date = Column(DateTime, default=None)
