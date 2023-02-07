from abc import ABC, abstractmethod


class AbstractCache(ABC):
    @abstractmethod
    def __init__(self, cache_client) -> None:
        self.cache_client = cache_client

    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, expire_time: int = 5):
        raise NotImplementedError

    @abstractmethod
    async def clear(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def is_cached(self, key: str):
        raise NotImplementedError
