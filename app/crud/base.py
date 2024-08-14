from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import (
    CANNOT_DELETE_INVESTED_PROJECT, CANNOT_UPDATE_FULLY_INVESTED_PROJECT,
    CANT_SET_LESS_THAN_ALREADY_DONATED, GET_OBJECT_ERROR, NOT_IN_DB
)
from app.models.user import User
from app.utils import db_change


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
        if db_obj.fully_invested == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANNOT_UPDATE_FULLY_INVESTED_PROJECT
            )
        if db_obj.invested_amount > obj.full_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANT_SET_LESS_THAN_ALREADY_DONATED
            )
        update_data = obj.dict(exclude_unset=True)
        for field in jsonable_encoder(db_obj):
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
        for invest in investments:
            obj, invest = await self.money_distribution(obj, invest)
            objects_to_add.append(obj)
            objects_to_add.append(invest)
        return await db_change(
            obj, session, self.model, add_list=objects_to_add
        )

    async def money_distribution(
            self,
            obj,
            invest
    ):
        object_remain = obj.full_amount - obj.invested_amount
        invest_remain = invest.full_amount - invest.invested_amount
        if object_remain > invest_remain:
            obj.invested_amount += invest_remain
            invest = await self.close_query(invest)
        elif object_remain == invest_remain:
            obj = await self.close_query(obj)
            invest = await self.close_query(invest)
        else:
            invest.invested_amount += object_remain
            obj = await self.close_query(obj)
        return obj, invest

    @staticmethod
    async def close_query(
            db_obj
    ):
        db_obj.invested_amount = db_obj.full_amount
        db_obj.fully_invested = True
        db_obj.close_date = datetime.utcnow()
        return db_obj
