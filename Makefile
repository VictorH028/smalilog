PYTHON ?= python3

.PHONY: install test compile check clean

install:
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) -m pytest -q

compile:
	$(PYTHON) -m compileall -q src

check: compile
	$(PYTHON) -m pytest -q

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache
