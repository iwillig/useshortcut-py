.DEFAULT_GOAL := test

.PHONY: install
install:
	pipenv install --dev

.PHONY: test
test: install
	pipenv run pytest -v

.PHONY: format
format:
	pipenv run black .

.PHONY: lint
lint:
	pipenv run black --check .

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache build dist *.egg-info

.PHONY: build
build: clean
	python setup.py sdist bdist_wheel

.PHONY: shell
shell:
	pipenv shell
