from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, delete, update, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.schemas import JWTData
from src.database import get_session
from src.models import Posts, UserPostReaction
from src.posts.schemas import PostSchema, PostOutSchema, PostUpdateSchema
from src.posts.redis import (
    get_likes_count,
    get_dislikes_count,
    increase_likes_count,
    decrease_dislikes_count,
    decrease_likes_count,
    increase_dislikes_count,
)


class PostService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_post(self, post: PostSchema, owner_id: int):
        query = insert(Posts).values(
            title=post.title, content=post.content, owner=owner_id
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_posts(self, jwt_data: JWTData):
        query = select(Posts, UserPostReaction).outerjoin(
            UserPostReaction,
            and_(
                Posts.id == UserPostReaction.post_id,
                UserPostReaction.user_id == jwt_data.user_id,
            ),
        )

        posts = await self.session.execute(query)
        post_data = []
        for post, reaction in posts:
            likes_count = get_likes_count(post.id)
            dislike_count = get_dislikes_count(post.id)
            post_data.append(
                PostOutSchema(
                    title=post.title,
                    content=post.content,
                    owner=post.owner,
                    like=reaction.like if reaction else False,
                    dislike=reaction.dislike if reaction else False,
                    likes_count=likes_count,
                    dislike_count=dislike_count,
                )
            )

        return post_data

    async def get_post(self, post_id: id, jwt_data: JWTData):
        query = (
            select(Posts, UserPostReaction)
            .outerjoin(
                UserPostReaction,
                and_(
                    Posts.id == UserPostReaction.post_id,
                    UserPostReaction.user_id == jwt_data.user_id,
                ),
            )
            .where(Posts.id == post_id)
        )
        post = await self.session.execute(query)
        post = post.one_or_none()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        likes_count = get_likes_count(post_id)
        dislike_count = get_dislikes_count(post_id)

        return PostOutSchema(
            title=post[0].title,
            content=post[0].content,
            owner=post[0].owner,
            like=post[1].like if post[1] else False,
            dislike=post[1].dislike if post[1] else False,
            likes_count=likes_count,
            dislike_count=dislike_count,
        )

    async def delete_post(self, post_id):
        query = delete(Posts).where(Posts.id == post_id)
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found.",
            )
        await self.session.commit()

    async def update_post(self, post_id, post: PostUpdateSchema):
        query = (
            update(Posts)
            .where(Posts.id == post_id)
            .values(post.dict())
            .returning(Posts)
        )
        post = await self.session.scalar(query)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found.",
            )
        await self.session.commit()
        return PostSchema.from_orm(post)

    async def check_permission(self, post_id: int, jwt_data: JWTData):
        post = await self.get_post(post_id, jwt_data)
        if jwt_data.user_id == post.owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

    async def get_reaction(self, post_id: int, jwt_data: JWTData):
        await self.check_permission(post_id, jwt_data)
        query = select(UserPostReaction).where(
            UserPostReaction.post_id == post_id,
            UserPostReaction.user_id == jwt_data.user_id,
        )
        reaction = await self.session.scalar(query)
        if reaction:
            return reaction

    async def dislike(self, post_id: int, jwt_data: JWTData):
        await self.check_permission(post_id, jwt_data)
        reaction = await self.get_reaction(post_id, jwt_data)
        if not reaction:
            query = UserPostReaction(
                user_id=jwt_data.user_id, post_id=post_id, dislike=True
            )
            self.session.add(query)
            increase_dislikes_count(post_id)
        elif reaction.dislike:
            query = (
                update(UserPostReaction)
                .values(dislike=False, like=False)
                .where(
                    UserPostReaction.post_id == post_id,
                    UserPostReaction.user_id == jwt_data.user_id,
                )
            )
            await self.session.execute(query)
            decrease_dislikes_count(post_id)
        else:
            query = (
                update(UserPostReaction)
                .values(dislike=True, like=False)
                .where(
                    UserPostReaction.post_id == post_id,
                    UserPostReaction.user_id == jwt_data.user_id,
                )
            )
            await self.session.execute(query)
            increase_dislikes_count(post_id)
            if reaction.like:
                decrease_likes_count(post_id)
        await self.session.commit()

    async def like(self, post_id: int, jwt_data: JWTData):
        await self.check_permission(post_id, jwt_data)
        reaction = await self.get_reaction(post_id, jwt_data)
        if not reaction:
            query = UserPostReaction(
                user_id=jwt_data.user_id, post_id=post_id, like=True
            )
            self.session.add(query)
            increase_likes_count(post_id)
        elif reaction.like:
            query = (
                update(UserPostReaction)
                .values(dislike=False, like=False)
                .where(
                    UserPostReaction.post_id == post_id,
                    UserPostReaction.user_id == jwt_data.user_id,
                )
            )
            await self.session.execute(query)
            decrease_likes_count(post_id)
        else:
            query = (
                update(UserPostReaction)
                .values(dislike=False, like=True)
                .where(
                    UserPostReaction.post_id == post_id,
                    UserPostReaction.user_id == jwt_data.user_id,
                )
            )
            await self.session.execute(query)
            increase_likes_count(post_id)
            if reaction.dislike:
                decrease_dislikes_count(post_id)
        await self.session.commit()
