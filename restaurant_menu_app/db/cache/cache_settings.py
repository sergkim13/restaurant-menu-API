import redis  # type: ignore

from config import REDIS_DOCKER_HOST

pool = redis.ConnectionPool(
    host=f'{REDIS_DOCKER_HOST}',
    port=6379,
    db=0,
    decode_responses=True,
)
redis_client = redis.Redis(connection_pool=pool)
