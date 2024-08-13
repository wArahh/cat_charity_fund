from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.QRKot.models import CharityProject, Donation
from app.constaints import GET_OBJECT_ERROR, DB_CHANGE_ERROR, NOT_IN_DB
from app.users.models import User


async def db_change(
        obj,
        session: AsyncSession,
        model,
        delete=False
):
    try:
        if delete:
            await session.delete(obj)
            await session.commit()
        else:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
    except Exception as error:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=DB_CHANGE_ERROR.format(model=model.__name__.lower(), error=error)
        )
    return obj


class CrudBase:
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        try:
            get_object = await session.execute(
                select(self.model).where(
                    self.model.id == obj_id
                )
            )
            obj = get_object.scalars().first()
        except Exception as error:
            raise HTTPException(GET_OBJECT_ERROR.format(model=self.model.__name__.lower(), error=error))
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_IN_DB)
        return obj

    async def get_all(
            self,
            session: AsyncSession,
    ):
        try:
            get_all = await session.execute(
                select(self.model)
            )
        except Exception as error:
            raise HTTPException(GET_OBJECT_ERROR.format(model=self.model.__name__.lower(), error=error))
        return get_all.scalars().all()

    async def create(
            self,
            obj,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_data = obj.dict()
        if user is not None:
            obj_data['user_id'] = user.id
        return await db_change(self.model(**obj_data), session, self.model)

    async def update(
            self,
            db_obj_id: int,
            obj,
            session: AsyncSession,
    ):
        db_obj = await self.get(db_obj_id, session)
        obj_data = jsonable_encoder(db_obj)
        update_data = obj.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await db_change(db_obj, session, self.model)

    async def delete(
            self,
            db_obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await self.get(db_obj_id, session)
        return await db_change(db_obj, session, self.model, delete=True)


class CrudCharityProject(CrudBase):
    pass


class CrudDonation(CrudBase):
    pass


charity_project_crud = CrudCharityProject(CharityProject)
donation_crud = CrudDonation(Donation)
