from celery import Celery

from config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USER_ID

TASKS_BROKER_URL = f"amqp://{RABBITMQ_USER_ID}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"

celery_app = Celery("tasks", broker=TASKS_BROKER_URL, result_backend="rpc://")
