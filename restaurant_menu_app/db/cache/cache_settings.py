import aioredis

from config import REDIS_DB, REDIS_EXP, REDIS_HOST  # , REDIS_PORT

redis_client = aioredis.from_url(
    f'redis://{REDIS_HOST}',
    db=REDIS_DB,
)

# pool = redis.ConnectionPool(
#     host=f'{REDIS_HOST}',
#     port=f'{REDIS_PORT}',
#     db=f'{REDIS_DB}',
#     decode_responses=True,

# )
# redis_client = redis.Redis(connection_pool=pool)
EXPIRE_TIME = REDIS_EXP
