import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from restaurant_menu_app.database import SQLALCHEMY_DATABASE_URL, Base
from restaurant_menu_app.main import app, get_db


@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope='function')
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c
