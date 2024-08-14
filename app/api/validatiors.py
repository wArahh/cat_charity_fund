from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.QRKot.crud import charity_project_crud
from app.constaints import NAME_ALREADY_IN_USE


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    if await charity_project_crud.get_charity_project_by_name(
            charity_project_name,
            session
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_ALREADY_IN_USE
        )
