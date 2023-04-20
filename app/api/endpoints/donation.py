from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationFullDB,
                                  DonationShortDB)

from ..validators import (check_charity_project_exists,
                          check_charity_project_not_invested,
                          check_project_name_duplicate)

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    print(all_donations)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationShortDB],
    response_model_exclude_none=True
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    all_donations = await donation_crud.get_user_donations(user, session)
    return all_donations


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True
)
async def get_my_donations(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation = await donation_crud.create(donation, session, user)
    return donation
