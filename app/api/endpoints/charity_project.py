from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_not_invested,
                                check_full_great_invested,
                                check_project_is_close,
                                check_project_name_description,
                                check_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_projects_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity_projects = await charity_projects_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Создает благотворительный проект.
    """
    check_project_name_description(charity_project)
    await check_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_projects_crud.create(
        charity_project, session
    )
    return new_charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_charity_project_not_invested(charity_project, session)
    charity_project = await charity_projects_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать, также нельзя установить требуемую
    сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    check_project_is_close(charity_project)
    check_project_name_description(obj_in)
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_full_great_invested(charity_project, obj_in.full_amount)
    charity_project = await charity_projects_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
