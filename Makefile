install:
	python3 -m venv venv
	./venv/bin/pip install matplotlib mypy flake8

run:
	./venv/bin/python3 fly_in.py $(ARGS)

debug:
	./venv/bin/python3 -m pdb fly_in.py $(ARGS)

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
