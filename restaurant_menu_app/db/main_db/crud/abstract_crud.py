from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractCRUD(ABC):
    @abstractmethod
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def read_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def read(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError
