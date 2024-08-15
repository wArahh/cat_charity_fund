from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class Funding(Base):
    __abstract__ = True
    full_amount = Column(
        Integer,
        CheckConstraint('full_amount > 0'),
    )
    invested_amount = Column(
        Integer,
        CheckConstraint(
            'invested_amount >= 0 and invested_amount <= full_amount'
        ),
        default=0,
    )
    fully_invested = Column(
        Boolean,
        default=False,
    )
    create_date = Column(
        DateTime,
        default=datetime.utcnow,
    )
    close_date = Column(
        DateTime,
    )

    def __repr__(self):
        return (
            f'<Funding need = {self.full_amount} '
            f'already_donated = {self.invested_amount}>'
            f'create_date = {self.create_date}>'
        )
