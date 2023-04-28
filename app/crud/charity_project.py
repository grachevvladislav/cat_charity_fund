from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProjects(CRUDBase):
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


charity_projects_crud = CRUDCharityProjects(CharityProject)
