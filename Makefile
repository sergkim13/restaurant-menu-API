install:
	poetry install

migration:
	poetry run alembic upgrade head

start:
	poetry run uvicorn restaurant_menu_app.main:app --reload

lint:
	poetry run flake8 restaurant_menu_app

compose:
	docker compose --env-file .docker.env up -d

stop:
	docker compose --env-file .docker.env down

compose-test:
	docker compose --env-file .docker-test.env -f docker-compose.test.yml -p testing up -d

stop-test:
	docker compose --env-file .docker-test.env -f docker-compose.test.yml -p testing down

hooks:
	poetry run pre-commit run --all-files

test:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov-report term-missing --cov=restaurant_menu_app --cov-report xml

rabbit:
	docker compose --env-file .env -f docker-compose.rabbit.yml up -d
