import aioredis

from config import REDIS_DB, REDIS_EXP, REDIS_HOST  # , REDIS_PORT

redis_client = aioredis.from_url(
    f"redis://{REDIS_HOST}",
    db=REDIS_DB,
)

EXPIRE_TIME = REDIS_EXP
