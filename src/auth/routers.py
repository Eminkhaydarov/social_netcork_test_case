from fastapi import APIRouter, Depends
from starlette import status
from .schemas import UserSchema, UserIn
from .service import AuthService

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def create_user(user_data: UserIn, service: AuthService = Depends()):
    user = await service.create_user(user_data)
    return UserSchema.from_orm(user)
