from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.constaints import DB_CHANGE_ERROR


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
