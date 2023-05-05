from datetime import datetime
import logging
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)
from app.crud.charity_project import charity_projects_crud

router = APIRouter()


@router.post(
    '/',
    response_model=list[dict[str, str]],
    #dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    projects = await charity_projects_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    logging.info(f'https://docs.google.com/spreadsheets/d/{spreadsheetid}')
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, projects, wrapper_services
    )
    return projects