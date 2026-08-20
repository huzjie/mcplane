.PHONY: install test lint serve doctor clean

install:
	pip install -e ".[test]"

test:
	pytest

lint:
	python -m compileall mcplane tests

serve:
	mcplane serve

doctor:
	mcplane doctor

clean:
	rm -rf dist build *.egg-info .pytest_cache __pycache__
