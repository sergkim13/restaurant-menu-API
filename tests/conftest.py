import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from config import DB_HOST, DB_PASS, DB_PORT, DB_USER, TEST_DB_NAME
from restaurant_menu_app.db.main_db.database import Base, get_db
from restaurant_menu_app.main import app

SQLALCHEMY_TEST_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}'


@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope='function')
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)

    yield db

    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c
