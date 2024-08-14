from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.QRKot.models import CharityProject, Donation
from app.constaints import GET_OBJECT_ERROR, DB_CHANGE_ERROR, NOT_IN_DB, CANNOT_DELETE_INVESTED_PROJECT, CANT_SET_LESS_THAN_ALREADY_DONATED
from app.users.models import User


async def db_change(
        obj,
        session: AsyncSession,
        model,
        delete=False,
        add_list=None
):
    try:
        if delete:
            await session.delete(obj)
            await session.commit()
        else:
            if add_list:
                session.add_all(add_list)
            else:
                session.add(obj)
            await session.commit()
            await session.refresh(obj)
    except Exception as error:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=DB_CHANGE_ERROR.format(
                model=model.__name__.lower(),
                error=error
            )
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
        except Exception as error:
            raise HTTPException(
                GET_OBJECT_ERROR.format(
                    model=self.model.__name__.lower(),
                    error=error
                )
            )
        obj = get_object.scalars().first()
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=NOT_IN_DB
            )
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
            raise HTTPException(
                GET_OBJECT_ERROR.format(
                    model=self.model.__name__.lower(),
                    error=error
                )
            )
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
        if db_obj.invested_amount > obj.full_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANT_SET_LESS_THAN_ALREADY_DONATED
            )
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
        if db_obj.invested_amount > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANNOT_DELETE_INVESTED_PROJECT
            )
        return await db_change(db_obj, session, self.model, delete=True)

    async def donation_processing(
            self,
            obj,
            db_model,
            session: AsyncSession
    ):
        try:
            available_investments = await session.execute(
                select(db_model).where(
                    db_model.fully_invested == 0
                ).order_by(db_model.create_date)
            )
        except Exception as error:
            raise HTTPException(
                GET_OBJECT_ERROR.format(
                    model=self.model.__name__.lower(),
                    error=error
                )
            )
        investments = available_investments.scalars().all()
        objects_to_add = []
        for db_query in investments:
            obj, db_query = await self.money_distribution(obj, db_query)
            objects_to_add.append(obj)
            objects_to_add.append(db_query)
        return await db_change(
            obj, session, self.model, add_list=objects_to_add
        )

    async def money_distribution(
            self,
            obj,
            db_obj
    ):
        object_remain = obj.full_amount - obj.invested_amount
        db_obj_remain = db_obj.full_amount - db_obj.invested_amount
        if object_remain > db_obj_remain:
            obj.invested_amount += db_obj_remain
            db_obj = await self.close_query(db_obj)
        elif object_remain == db_obj_remain:
            obj = await self.close_query(obj)
            db_obj = await self.close_query(db_obj)
        else:
            db_obj.invested_amount += object_remain
            obj = await self.close_query(obj)
        return obj, db_obj

    @staticmethod
    async def close_query(
            db_obj
    ):
        db_obj.invested_amount = db_obj.full_amount
        db_obj.fully_invested = True
        db_obj.close_date = datetime.utcnow()
        return db_obj


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


class CrudDonation(CrudBase):
    @staticmethod
    async def get_user_donations(
            user_id: int,
            session: AsyncSession,
    ):
        get_user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        return get_user_donations.scalars().all()


charity_project_crud = CrudCharityProject(CharityProject)
donation_crud = CrudDonation(Donation)
