.DEFAULT_GOAL := test

.PHONY: install
install:
	poetry install

.PHONY: test
test: install
	poetry run pytest -v
