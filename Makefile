PYTHON ?= python3

.PHONY: install test compile check native clean

# Requerido antes de `make test`: los tests importan `smalilog.*` desde src/.
install:
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) -m pytest -q

compile:
	$(PYTHON) -m compileall -q src

check: compile
	$(PYTHON) -m pytest -q

# Compila liblogger.so y la deja en build_payloads/lib/<abi>/.
native:
	$(MAKE) -C bin/native_lib

clean:
	rm -rf build dist *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache
	$(MAKE) -C bin/native_lib clean
