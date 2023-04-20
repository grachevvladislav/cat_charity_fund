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
            status_code=422,
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
            status_code=404,
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
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=422,
            detail=('Нельзя удалить проект, в который уже были инвестированы '
                    'средства, его можно только закрыть!')
        )

#
#
# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservations)
#         )
#
#
# async def check_reservation_before_edit(
#     reservation_id: int,
#     session: AsyncSession,
#     user: User
# ) -> Reservation:
#     reservation = await reservation_crud.get(
#         obj_id=reservation_id, session=session
#     )
#     if reservation.user_id != user.id and not user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     if not reservation:
#         raise HTTPException(status_code=404, detail='Бронь не найдена!')
#     return reservation
