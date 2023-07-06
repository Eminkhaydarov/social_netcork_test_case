from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models import User
from src.auth.schemas import UserIn, UserSchema
from src.auth.security import get_password_hash
from src.database import get_session


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user(self, user_data: UserIn) -> User | None:
        user_data = await self.validate_create_user(user_data)
        insert_query = (
            insert(User)
            .values(
                {
                    "email": user_data.email,
                    "username": user_data.username,
                    "hashed_password": get_password_hash(user_data.password),
                }
            )
            .returning(User)
        )
        user = await self.session.scalar(insert_query)
        await self.session.commit()
        return user

    async def get_user_by_username(self, username: str) -> UserSchema:
        query = select(User).where(User.username == username)
        user = await self.session.execute(query)
        user = user.scalar_one_or_none()
        return user

    async def validate_create_user(self, user_data: UserIn) -> UserIn:
        user = await self.get_user_by_username(user_data.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists.",
            )
        return user_data
