import datetime
from typing import Optional

from sqlalchemy import select, func, text, column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


class CRUDCharityProjects(CRUDBase):
    async def create(
        self,
        project,
        session: AsyncSession
    ):
        prj_data = project.dict()
        prj_data['invested_amount'] = 0

        donations = await session.execute(
            select(Donation).where(Donation.fully_invested == 0)
        )
        donations = donations.scalars().all()

        for donation in donations:
            project_need = prj_data['full_amount'] - prj_data['invested_amount']
            donation_size = donation.full_amount - donation.invested_amount
            if donation_size >= project_need:
                prj_data['invested_amount'] = prj_data['full_amount']
                prj_data['fully_invested'] = True
                prj_data['close_date'] = datetime.datetime.now()

                donation.invested_amount += donation_size
                if project_need == donation_size:
                    donation.fully_invested = True
                    donation.close_date = datetime.datetime.now()
                session.add(donation)
                break
            else:
                prj_data['invested_amount'] += project_need
                donation.invested_amount = project.full_amount
                donation.fully_invested = True
                donation.close_date = datetime.datetime.now()
                session.add(project)

        db_obj = self.model(**prj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_prject_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        project_name_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_name_id = project_name_id.scalars().first()
        return project_name_id

    async def get_projects_by_completion_rate(self,
        session: AsyncSession,
    ) -> list[dict[str, str]]:
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.description,
                (
                    func.julianday(CharityProject.close_date)
                    - func.julianday(CharityProject.create_date)
                ).label('collection_time')
            ).where(
                CharityProject.fully_invested == 1
            ).order_by(
                (func.julianday(CharityProject.close_date)
                 - func.julianday(CharityProject.create_date)).desc()
            )
        )
        projects = projects.all()
        return projects


charity_projects_crud = CRUDCharityProjects(CharityProject)
