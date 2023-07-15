from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import event

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    username = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)
    full_name = sa.Column(sa.String, nullable=True)
    location = sa.Column(sa.String, nullable=True)
    company = sa.Column(sa.String, nullable=True)


class Posts(Base):
    __tablename__ = "post"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    content = sa.Column(sa.String)
    owner = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))


class UserPostReaction(Base):
    __tablename__ = "user_post_reaction"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
    post_id = sa.Column(sa.Integer, sa.ForeignKey("post.id", ondelete="CASCADE"))
    like = sa.Column(sa.Boolean, default=False)
    dislike = sa.Column(sa.Boolean, default=False)
