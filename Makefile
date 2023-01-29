install:
	poetry install

prepare-migrations:
	poetry run alembic init migrations

migration:
	poetry run alembic revision --autogenerate -m 'Creating tables'
	poetry run alembic upgrade head

start:
	poetry run uvicorn restaurant_menu_app.main:app --reload

lint:
	poetry run flake8 restaurant_menu_app

compose:
	docker compose up -d

compose-stop:
	docker compose down

compose-test:
	docker compose -f docker-compose.test.yml -p testing up -d

hooks:
	poetry run pre-commit run --all-files

test:
	poetry run pytest -vv