from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.models import User
from src.auth.schemas import UserIn, UserSchema
from src.auth.security import get_password_hash
from src.database import get_session
from src.auth.verify_email import verify_email
from src.auth.clearbit import get_additional_data


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user(self, user_data: UserIn) -> User | None:
        if await verify_email(user_data.email):
            try:
                data = {
                    "email": user_data.email,
                    "username": user_data.username,
                    "hashed_password": get_password_hash(user_data.password),
                }
                additional_data = await get_additional_data(user_data.email)
                insert_query = (
                    insert(User).values(data | additional_data).returning(User)
                )
                user = await self.session.scalar(insert_query)
                await self.session.commit()
            except IntegrityError as e:
                await self.session.rollback()
                error_info = str(e.orig)
                if "username" in error_info:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already exists.",
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already exists.",
                    )
        return user

    async def get_user_by_username(self, username: str) -> UserSchema:
        query = select(User).where(User.username == username)
        user = await self.session.execute(query)
        user = user.scalar_one_or_none()
        return user
