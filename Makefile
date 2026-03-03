PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt
REQUIREMENTS = requirements.txt

all: run

install:
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf .mypy_cache .pytest_cache .DS_Store mazegen/.DS_Store
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +


lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .

build:
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

install-pkg: build
	$(PYTHON) -m pip install dist/*.whl

.PHONY: all install run debug clean lint lint-strict build install-pkg