from sqlalchemy.ext.asyncio import AsyncSession


class ServiceMixin:
    def __init__(self, db: AsyncSession):
        self.db = db
