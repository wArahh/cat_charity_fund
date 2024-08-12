from sqlalchemy import Column, String, CheckConstraint, Text, Integer, Boolean, DateTime
from datetime import datetime

from app.core.db import Base


class Funding(Base):
    __abstract__ = True
    full_amount = Column(
        Integer,
        CheckConstraint('full_amount > 0'),
    )
    invested_amount = Column(
        Integer,
        CheckConstraint('invested_amount >= 0'),
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


class CharityProject(Funding):
    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )
    description = Column(
        Text,
        nullable=False,
    )


class Donation(Funding):
    # todo user_id
    comment = Column(
        Text
    )
