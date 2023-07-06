from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import event

from sqlalchemy.orm import declarative_base

from src.posts.redis import (
    increase_likes_count,
    decrease_dislikes_count,
    increase_dislikes_count,
    decrease_likes_count,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    username = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)


class Posts(Base):
    __tablename__ = "post"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    content = sa.Column(sa.String, unique=True)
    owner = sa.Column(sa.Integer, sa.ForeignKey("user.id"))


class UserPostReaction(Base):
    __tablename__ = "user_post_reaction"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"))
    post_id = sa.Column(sa.Integer, sa.ForeignKey("post.id", ondelete="CASCADE"))
    like = sa.Column(sa.Boolean, default=False)
    dislike = sa.Column(sa.Boolean, default=False)

