install:
	poetry install

prepare-migrations:
	poetry run alembic init migrations

migrations:
	poetry run alembic revision --autogenerate -m 'Creating tables'
	poetry run alembic upgrade head

start:
	poetry run uvicorn restaurant_menu_app.main:app --reload

lint:
	poetry run flake8 restaurant_menu_app