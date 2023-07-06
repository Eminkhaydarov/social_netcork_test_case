from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from src.config import setting
from src.auth.models import User
from src.auth.schemas import Token, JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)


def create_access_token(user: User, expires_delta: timedelta | None = None):
    to_encode = {"sub": user.username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "user_id": user.id})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt


async def parse_jwt_data(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> JWTData | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = JWTData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data
