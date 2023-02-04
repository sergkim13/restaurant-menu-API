import json

from fastapi.encoders import jsonable_encoder

from .cache_settings import EXPIRE_TIME, redis_client


async def get_cache(key_prefix, key_body):
    key = generate_key(key_prefix, key_body)
    value = await redis_client.get(key)
    return json.loads(value)


async def set_cache(key_prefix, key_body, value):
    key = generate_key(key_prefix, key_body)
    value = json.dumps(jsonable_encoder(value))
    await redis_client.set(key, value, ex=EXPIRE_TIME)


async def clear_cache(key_prefix, key_body):
    key = generate_key(key_prefix, key_body)
    await redis_client.delete(key)


def generate_key(key_prefix, key_body):
    key = f"{key_prefix}:{key_body}"
    return key


async def is_cached(key_prefix, key_body):
    key = generate_key(key_prefix, key_body)
    return await redis_client.exists(key)
