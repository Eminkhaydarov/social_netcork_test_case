from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.auth.jwt import parse_jwt_data
from src.auth.schemas import JWTData
from src.posts.services import PostService
from src.posts.schemas import PostOutSchema, PostUpdateSchema, PostSchema

post_router = APIRouter()


@post_router.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts(
    jwt_data: JWTData = Depends(parse_jwt_data), service: PostService = Depends()
):
    posts = await service.get_posts(jwt_data)
    return posts


@post_router.get(
    "/posts/{post_id}", response_model=PostOutSchema, status_code=status.HTTP_200_OK
)
async def get_post(
    post_id: int,
    jwt_data: JWTData = Depends(parse_jwt_data),
    service: PostService = Depends(),
):
    post = await service.get_post(post_id, jwt_data)
    return post


@post_router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(
    post_id: int,
    jwt_data: JWTData = Depends(parse_jwt_data),
    service: PostService = Depends(),
):
    await service.check_permission(post_id, jwt_data)
    await service.delete_post(post_id)


@post_router.patch(
    "/posts/{post_id}",
    response_model=PostSchema,
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post: PostUpdateSchema,
    post_id: int,
    jwt_data: JWTData = Depends(parse_jwt_data),
    service: PostService = Depends(),
):
    await service.check_permission(post_id, jwt_data)
    post = await service.update_post(post_id, post)
    return post


@post_router.post("/posts/{post_id}/like", status_code=status.HTTP_200_OK)
async def like(
    post_id: int,
    jwt_data: JWTData = Depends(parse_jwt_data),
    service: PostService = Depends(),
):
    await service.like(post_id, jwt_data)


@post_router.post("/posts/{post_id}/dislike", status_code=status.HTTP_200_OK)
async def dislike(
    post_id: int,
    jwt_data: JWTData = Depends(parse_jwt_data),
    service: PostService = Depends(),
):
    await service.dislike(post_id, jwt_data)


@post_router.post("/posts", status_code=status.HTTP_200_OK)
async def create_post(
    post: PostSchema,
    jwt_data: JWTData = Depends(parse_jwt_data),
    service: PostService = Depends(),
):
    await service.create_post(post, jwt_data.user_id)
