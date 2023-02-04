import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists

from config import DB_HOST, DB_PASS, DB_PORT, DB_USER, TEST_DB_NAME
from restaurant_menu_app.db.cache.cache_settings import redis_client
from restaurant_menu_app.db.main_db import crud
from restaurant_menu_app.db.main_db.database import Base, get_db
from restaurant_menu_app.main import app
from restaurant_menu_app.schemas import scheme
from tests.fixtures.dishes_fixtures import new_dish
from tests.fixtures.menus_fixtures import new_menu
from tests.fixtures.submenus_fixtures import new_submenu

# Test database fixtures
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

    if not database_exists:
        create_database(engine.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope="function")
async def db(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    db = AsyncSession(bind=connection)

    yield db

    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db):
    app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# CRUD fixtures
@pytest_asyncio.fixture
async def fixture_menu(db):
    menu = await crud.create_menu(scheme.MenuCreate(**new_menu), db)
    return await crud.read_menu(menu.id, db)


@pytest_asyncio.fixture
async def fixture_submenu(db, fixture_menu):
    menu = fixture_menu
    submenu = await crud.create_submenu(
        menu.id,
        scheme.SubmenuCreate(**new_submenu),
        db,
    )
    return menu.id, await crud.read_submenu(menu.id, submenu.id, db)


@pytest_asyncio.fixture
async def fixture_dish(db, fixture_menu, fixture_submenu):
    menu = fixture_menu
    submenu = fixture_submenu[1]
    dish = await crud.create_dish(submenu.id, scheme.DishCreate(**new_dish), db)
    return menu.id, submenu.id, await crud.read_dish(menu.id, submenu.id, dish.id, db)


# Auto clearing cache fixture
@pytest_asyncio.fixture(scope="function", autouse=True)
async def clear_cache():
    await redis_client.flushdb()
