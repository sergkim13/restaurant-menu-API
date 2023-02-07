import json

from aioredis.client import Redis
from fastapi.encoders import jsonable_encoder

from restaurant_menu_app.db.cache.abstract_cache import AbstractCache

from .cache_settings import EXPIRE_TIME, redis_client


class Cache(AbstractCache):
    def __init__(self, cache_client: Redis) -> None:
        self.redis_client = cache_client

    async def get(self, key: str):
        value = await self.redis_client.get(key)
        return json.loads(value)

    async def set(self, key: str, value: str, expire_time=EXPIRE_TIME):
        value = json.dumps(jsonable_encoder(value))
        await self.redis_client.set(key, value, expire_time)

    async def clear(self, key: str):
        await self.redis_client.delete(key)

    async def is_cached(self, key: str):
        return await self.redis_client.exists(key)


def get_cache():
    return Cache(cache_client=redis_client)
