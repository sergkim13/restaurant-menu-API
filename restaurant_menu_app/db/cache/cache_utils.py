import json

from fastapi.encoders import jsonable_encoder

from .cache_settings import redis_client


def get_cache(key_prefix, key_body):
    key = generate_key(key_prefix, key_body)
    value = redis_client.get(key)
    return json.loads(value)


def set_cache(key_prefix, key_body, value):
    key = generate_key(key_prefix, key_body)
    value = json.dumps(jsonable_encoder(value))
    redis_client.set(key, value)


def clear_cache(key_prefix, key_body):
    key = generate_key(key_prefix, key_body)
    for key in redis_client.scan_iter(f'{key}*'):
        redis_client.delete(key)


def generate_key(key_prefix, key_body):
    key = f'{key_prefix}:{key_body}'
    return key


def is_cached(key_prefix, key_body):
    key = generate_key(key_prefix, key_body)
    return redis_client.exists(key)
