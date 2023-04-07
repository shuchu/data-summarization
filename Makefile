
format: 
	python -m isort ./summ/ summerizer.py
	python -m black --target-version py39 ./summ/ summerizer.py

lint:
	python -m mypy ./summ/ ./summerizer.py
	python -m isort ./summ/ summerizer.py --check-only
	python -m flake8 ./summ/ summerizer.py
	python -m black --check ./summ/ summerizer.py

test:
	python -m pytest ./tests

build:
	bazel build summerizer

clean:
	bazel clean --expunge
