from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    username = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)

