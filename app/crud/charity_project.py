from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import GET_OBJECT_ERROR
from app.crud.base import CrudBase
from app.models import CharityProject


class CrudCharityProject(CrudBase):
    @staticmethod
    async def get_charity_project_by_name(
            charity_name: str,
            session: AsyncSession,
    ):
        try:
            get_charity_project_name = await session.execute(
                select(CharityProject).where(
                    CharityProject.name == charity_name
                )
            )
        except Exception as error:
            raise HTTPException(
                GET_OBJECT_ERROR.format(
                    model=CharityProject.__name__.lower(),
                    error=error
                )
            )
        return get_charity_project_name.scalars().first()


charity_project_crud = CrudCharityProject(CharityProject)
