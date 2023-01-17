install:
	poetry install

prepare-migrations:
	alembic init migrations

migrations:
	alembic revision --autogenerate -m 'Creating tables'
	alembic upgrade head

start:
	poetry run uvicorn restaurant_menu_app.main:app --reload

lint:
	poetry run flake8 restaurant_menu_app