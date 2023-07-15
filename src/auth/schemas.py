import re

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PASSWORD_MATCH_PATTERN = re.compile(r"^([a-zA-Z0-9@*#]{4,16})$")


class Token(BaseModel):
    access_token: str
    token_type: str


class JWTData(BaseModel):
    username: str | None = None
    user_id: int | None = None


class UserSchema(BaseModel):
    username: str
    email: EmailStr

    @validator("username")
    def validate_username(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    class Config:
        orm_mode = True


class UserIn(UserSchema):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if not PASSWORD_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Password requirements not met. Please use 4 to 16 characters, including letters (both "
                "uppercase and lowercase), numbers, '@', '*', or '#'.",
            )
        return value


class UserOutSchema(UserSchema):
    full_name: str | None = None
    location: str | None = None
    company: str | None = None

    class Config:
        orm_mode = True
