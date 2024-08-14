from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.QRKot.models import CharityProject
from app.QRKot.crud import donation_crud
from app.QRKot.serializers import CreateDonation, CertainDonationDB, DonationDB
from app.core.user import current_user, current_superuser
from app.users.models import User

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
) -> list[DonationDB]:
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=list[CertainDonationDB],
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> list[CertainDonationDB]:
    return await donation_crud.get_user_donations(user.id, session)


@router.post(
    '/',
    response_model=CertainDonationDB,
)
async def create_donation(
        donation: CreateDonation,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.create(
        donation, session, user
    )
    return await donation_crud.donation_processing(
        donation, CharityProject, session
    )
