from sqlalchemy import Column, ForeignKey, Integer, Text

from .dase import CharityDonationBase


class Donation(CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)
