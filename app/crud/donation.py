import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, User


class CRUDDonation(CRUDBase):
    async def create(
        self,
        donation,
        session: AsyncSession,
        user: User,
        donation_data=None
    ):
        donation_data = donation.dict()
        donation_data['user_id'] = user.id
        donation_data['invested_amount'] = 0

        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 0)
        )
        projects = projects.scalars().all()

        for project in projects:
            donation_size = (donation_data['full_amount'] -
                             donation_data['invested_amount'])
            project_need = project.full_amount - project.invested_amount
            if project_need >= donation_size:
                donation_data['invested_amount'] = donation_data['full_amount']
                donation_data['fully_invested'] = True
                donation_data['close_date'] = datetime.datetime.now()

                project.invested_amount += donation_size
                if project_need == donation_size:
                    project.fully_invested = True
                    project.close_date = datetime.datetime.now()
                session.add(project)
                break
            else:
                donation_data['invested_amount'] += project_need
                project.invested_amount = project.full_amount
                project.fully_invested = True
                project.close_date = datetime.datetime.now()
                session.add(project)

        db_obj = self.model(**donation_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession,
    ):
        user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        user_donations = user_donations.scalars().all()
        return user_donations


donation_crud = CRUDDonation(Donation)
