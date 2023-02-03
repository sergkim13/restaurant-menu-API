import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists

from config import DB_HOST, DB_PASS, DB_PORT, DB_USER, TEST_DB_NAME
from restaurant_menu_app.db.main_db.database import Base, get_db
from restaurant_menu_app.main import app

SQLALCHEMY_TEST_DATABASE_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}'
)


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine():
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

    if not database_exists:
        create_database(engine.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope='function')
async def db(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    db = AsyncSession(bind=connection)

    yield db

    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope='function')
async def client(db):
    app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
