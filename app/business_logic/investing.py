from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.utils import db_change


async def donation_processing(target, db_obj, session: AsyncSession):
    sources = await CrudBase.get_available_investments(db_obj, session)
    objects_to_add = []
    for source in sources:
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        target.invested_amount += transfer_amount
        source.invested_amount += transfer_amount
        for item in (target, source):
            if item.invested_amount == item.full_amount:
                item.fully_invested = True
                item.close_date = datetime.utcnow()
        objects_to_add.extend([target, source])
    return await db_change(target, session, sources, add_list=objects_to_add)
