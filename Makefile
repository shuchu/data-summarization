
format: 
	python -m isort ./
	python -m black --target-version py39 ./

lint:
	python -m mypy ./
	python -m isort ./ --check-only
	python -m flake8 ./
	python -m black --check ./

test:
	python -m pytest ./tests
