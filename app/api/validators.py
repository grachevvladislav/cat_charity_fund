from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_projects_crud
from app.models.charity_project import CharityProject


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project = await charity_projects_crud.get_prject_id_by_name(
        project_name, session
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_projects_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого проекта не существует!'
        )
    return charity_project


async def check_charity_project_not_invested(
    charity_project: CharityProject,
    session: AsyncSession
) -> None:
    charity_project = await charity_projects_crud.get(
        charity_project.id, session
    )
    if charity_project.fully_invested or charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_project_name_description(project) -> None:
    project_data = project.dict()
    if 'name' in project_data and project_data['name'] is not None and (
            project_data['name'] == '' or len(project_data['name']) > 100
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Недопустимое имя проекта!'
        )
    if ('description' in project_data and
            (project_data['description'] == '')):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Недопустимое описание проекта!'
        )


def check_project_is_close(project) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_full_great_invested(project, full_amount) -> None:
    if project.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
