black:
	poetry run black src

mypy : 
	poetry run mypy src --ignore-missing-imports

lint:
	poetry run pylint src

isort:
	poetry run isort 