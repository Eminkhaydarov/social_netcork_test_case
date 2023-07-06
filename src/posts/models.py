import sqlalchemy as sa

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Posts(Base):
    __tablename__ = "post"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    content = sa.Column(sa.String, unique=True)
    owner = sa.Column(sa.Integer, sa.ForeignKey("user.id"))

class UserPostRelation(Base):
    __tablename__ = "user_post_relation"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"))
    post_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"))