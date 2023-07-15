from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class PostOutSchema(PostSchema):
    id: int
    owner: int
    like: bool | None = False
    dislike: bool | None = False
    likes_count: int
    dislike_count: int


class PostUpdateSchema(PostSchema):
    title: str | None = None
    content: str | None = None
