import os

from dotenv import load_dotenv
from pydantic import BaseSettings


class Setting(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


load_dotenv()

setting = Setting(
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=os.getenv("DB_PORT"),
    DB_NAME=os.getenv("DB_NAME"),
    DB_USER=os.getenv("DB_USER"),
    DB_PASS=os.getenv("DB_PASS"),
    SECRET_KEY=os.getenv("SECRET_KEY"),
    ALGORITHM=os.getenv("ALGORITHM"),
    ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
)
