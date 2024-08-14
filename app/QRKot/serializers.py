from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: int = Field(..., ge=1)


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = Field(False)
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class DonationBase(BaseModel):
    full_amount: int = Field(..., ge=1)
    comment: Optional[str] = None


class CreateDonation(DonationBase):
    pass


class CertainDonationDB(DonationBase):
    id: int
    create_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class DonationDB(CertainDonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool = Field(False)
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
