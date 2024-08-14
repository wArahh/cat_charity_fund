from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.QRKot.models import Donation
from app.QRKot.crud import charity_project_crud
from app.QRKot.serializers import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
from app.core.user import current_superuser
from app.api.validatiors import check_name_duplicate

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """ superuser access only """
    await check_name_duplicate(charity_project.name, session)
    project = await charity_project_crud.create(
        charity_project,
        session
    )
    return await charity_project_crud.donation_processing(
        project, Donation, session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        project_id: int,
        charity_project: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """ superuser access only """
    await check_name_duplicate(charity_project.name, session)
    return await charity_project_crud.update(
        project_id,
        charity_project,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """ superuser access only """
    return await charity_project_crud.delete(
        project_id,
        session
    )
