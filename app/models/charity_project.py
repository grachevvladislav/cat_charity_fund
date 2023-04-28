from sqlalchemy import Column, String, Text

from .dase import CharityDonationBase


class CharityProject(CharityDonationBase):
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
