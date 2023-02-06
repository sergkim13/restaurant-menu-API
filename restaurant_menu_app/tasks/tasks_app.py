from celery import Celery

from config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USER

TASKS_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"

celery_app = Celery("tasks", broker=TASKS_BROKER_URL, backend="rpc://", include=["restaurant_menu_app.tasks.tasks"])
