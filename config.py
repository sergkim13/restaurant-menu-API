import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

TEST_DB_NAME = os.environ.get("TEST_DB_NAME")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")
REDIS_EXP = os.environ.get("REDIS_EXP")

RABBITMQ_USER_ID = os.environ.get("RABBITMQ_USER_ID")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
