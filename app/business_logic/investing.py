from datetime import datetime


def donation_processing(
        target,
        sources,
):
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
