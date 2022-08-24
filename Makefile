black:
	poetry run black src

mypy : 
	poetry run mypy src 

lint:
	poetry run pylint src

isort:
	poetry run isort src