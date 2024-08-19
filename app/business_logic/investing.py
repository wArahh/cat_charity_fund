from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


def donation_processing(
        target: Union[CharityProject, Donation],
        sources: Union[List[Donation], List[CharityProject]],
) -> List[Union[CharityProject, Donation]]:
    objects_to_add = []
    target.invested_amount = target.invested_amount or 0
    target.full_amount = target.full_amount or 0
    for source in sources:
        if source.fully_invested:
            break
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for item in (target, source):
            item.invested_amount += transfer_amount
            if item.invested_amount == item.full_amount:
                item.fully_invested = True
                item.close_date = datetime.utcnow()
        objects_to_add.append(source)
    return objects_to_add
