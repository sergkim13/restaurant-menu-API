import json

import redis  # type: ignore
from fastapi.encoders import jsonable_encoder

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True,
)
redis_client = redis.Redis(connection_pool=pool)


def get_cache(key):
    value = redis_client.get(key)
    return json.loads(value)


def set_cache(key, value):
    value = json.dumps(jsonable_encoder(value))
    redis_client.set(key, value)


def clear_cache(key):
    for key in redis_client.scan_iter(f'{key}*'):
        redis_client.delete(key)


def is_cached(key):
    return redis_client.exists(key)
