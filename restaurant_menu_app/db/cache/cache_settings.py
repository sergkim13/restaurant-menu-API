import redis  # type: ignore

from config import REDIS_DB, REDIS_HOST, REDIS_PORT

pool = redis.ConnectionPool(
    host=f'{REDIS_HOST}',
    port=f'{REDIS_PORT}',
    db=f'{REDIS_DB}',
    decode_responses=True,
)
redis_client = redis.Redis(connection_pool=pool)
