from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .jwt import create_access_token
from .schemas import UserSchema, UserIn
from .security import verify_password
from .service import AuthService

auth_router = APIRouter()


@auth_router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def create_user(user_data: UserIn, service: AuthService = Depends()):
    user = await service.create_user(user_data)
    return UserSchema.from_orm(user)


@auth_router.post("/users/tokens", status_code=status.HTTP_200_OK)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: AuthService = Depends(),
):
    user = await service.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

