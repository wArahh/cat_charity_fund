from fastapi_users import schemas
from fastapi import status, HTTPException
from pydantic import validator
import re
from app.constaints import INCORRECT_REGEX, ACCEPTED_REGEX


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):

    @validator('password')
    def validate_password(cls, password):
        if not re.match(ACCEPTED_REGEX, password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INCORRECT_REGEX
            )
        return password


class UserUpdate(schemas.BaseUserUpdate):
    pass
