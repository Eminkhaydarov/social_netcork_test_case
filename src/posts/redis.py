from src.database import get_redis_connection


def increase_likes_count(post_id: int):
    redis_conn = get_redis_connection()
    redis_conn.hincrby("post_likes", post_id, 1)


def get_likes_count(post_id: int):
    redis_conn = get_redis_connection()
    likes_count = redis_conn.hget("post_likes", post_id)
    return int(likes_count) if likes_count else 0


def increase_dislikes_count(post_id: int):
    redis_conn = get_redis_connection()
    redis_conn.hincrby("post_dislikes", post_id, 1)


def get_dislikes_count(post_id: int):
    redis_conn = get_redis_connection()
    dislikes_count = redis_conn.hget("post_dislikes", post_id)
    return int(dislikes_count) if dislikes_count else 0


def decrease_dislikes_count(post_id: int):
    redis_conn = get_redis_connection()
    redis_conn.hincrby("post_dislikes", post_id, -1)


def decrease_likes_count(post_id: int):
    redis_conn = get_redis_connection()
    redis_conn.hincrby("post_likes", post_id, -1)
