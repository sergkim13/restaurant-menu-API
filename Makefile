install:
	poetry install

start:
	poetry run uvicorn restaurant_menu_app.main:app --reload