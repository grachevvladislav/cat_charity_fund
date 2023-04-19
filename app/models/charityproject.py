from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship

from .dase import CharityDonationBase
from .donation import Donation


class CharityProject(CharityDonationBase):
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    invested_amount = Column(Integer)
    doations = relationship(Donation)
