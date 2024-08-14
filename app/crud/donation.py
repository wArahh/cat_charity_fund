from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import GET_OBJECT_ERROR
from app.crud.base import CrudBase
from app.models import Donation


class CrudDonation(CrudBase):
    @staticmethod
    async def get_user_donations(
            user_id: int,
            session: AsyncSession,
    ):
        try:
            get_user_donations = await session.execute(
                select(Donation).where(
                    Donation.user_id == user_id
                )
            )
        except Exception as error:
            raise HTTPException(
                GET_OBJECT_ERROR.format(
                    model=Donation.__name__.lower(),
                    error=error
                )
            )
        return get_user_donations.scalars().all()


donation_crud = CrudDonation(Donation)
