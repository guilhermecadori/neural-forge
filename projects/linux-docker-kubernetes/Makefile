.PHONY: install lint test train eval clean

install:
	pip install -e .

lint:
	ruff check src tests scripts

test:
	pytest tests

train:
	python scripts/run_train.py

eval:
	python scripts/run_eval.py

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache **/__pycache__
