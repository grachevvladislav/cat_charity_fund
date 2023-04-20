from sqlalchemy import Column, Integer, String, Text

from .dase import CharityDonationBase


class CharityProject(CharityDonationBase):
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    invested_amount = Column(Integer, default=0)
