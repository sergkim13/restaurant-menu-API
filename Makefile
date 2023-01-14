install:
	poetry install

start:
	poetry run uvicorn ylab_project.app:app --reload