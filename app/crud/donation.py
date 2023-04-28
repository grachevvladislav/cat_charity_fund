from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from app.crud.base import CRUDBase
from app.crud.charity_project import charity_projects_crud
from app.models import CharityProject, Donation, User
from app.schemas.charity_project import CharityProjectUpdate


class CRUDDonation(CRUDBase):
    async def create(
            self,
            donation,
            session: AsyncSession,
            user: User
    ):
        donation_data = donation.dict()
        donation_data['user_id'] = user.id
        donation_data['invested_amount'] = 0

        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 0)
        )
        projects = projects.scalars().all()

        for project in projects:
            project_data = {}
            donation_size = donation_data['full_amount'] - donation_data['invested_amount']
            print(donation_size)
            project_need = project.full_amount - project.invested_amount
            if project_need >= donation_size:
                donation_data['invested_amount'] = donation_data['full_amount']
                donation_data['fully_invested'] = True
                donation_data['close_date'] = datetime.datetime.now()

                project_data[
                    'invested_amount'
                ] = project.invested_amount + donation_size
                if project_need == donation_size:
                    project_data['fully_invested'] = True
                    project_data['close_date'] = datetime.datetime.now()

                project_upd = CharityProjectUpdate(**project_data)
                await charity_projects_crud.update(
                    project, project_upd, session
                )
                break
            else:
                donation_data['invested_amount'] += project_need

                project_data['invested_amount'] = project.full_amount
                project_data['fully_invested'] = True
                project_data['close_date'] = datetime.datetime.now()

                project_upd = CharityProjectUpdate(**project_data)
                await charity_projects_crud.update(
                    project, project_upd, session
                )
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
