from src.database import get_redis_connection


async def increase_likes_count(post_id: int):
    redis_conn = await get_redis_connection()
    async with redis_conn.client() as redis_client:
        await redis_client.hincrby("post_likes", post_id, 1)


# ...


async def get_likes_count(post_id: int):
    redis_conn = await get_redis_connection()
    async with redis_conn.client() as redis_client:
        likes_count = await redis_client.hget("post_likes", post_id)
    return int(likes_count) if likes_count else 0


# ...


async def increase_dislikes_count(post_id: int):
    redis_conn = await get_redis_connection()
    async with redis_conn.client() as redis_client:
        await redis_client.hincrby("post_dislikes", post_id, 1)


# ...


async def get_dislikes_count(post_id: int):
    redis_conn = await get_redis_connection()
    async with redis_conn.client() as redis_client:
        dislikes_count = await redis_client.hget("post_dislikes", post_id)
    return int(dislikes_count) if dislikes_count else 0


# ...


async def decrease_dislikes_count(post_id: int):
    redis_conn = await get_redis_connection()
    async with redis_conn.client() as redis_client:
        await redis_client.hincrby("post_dislikes", post_id, -1)


# ...


async def decrease_likes_count(post_id: int):
    redis_conn = await get_redis_connection()
    async with redis_conn.client() as redis_client:
        await redis_client.hincrby("post_likes", post_id, -1)
