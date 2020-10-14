.PHONY: lint test clean coverage docs build publish

# See setup.cfg for flake8 and mypy for options
lint:
	python -m black ./iso8583 ./tests
	python -m flake8
	python -m mypy

# See pyproject.toml for pytest options
test: lint
	python -m pytest

clean:
	$(MAKE) coverage-clean
	$(MAKE) build-clean

# Generage and publish code coverage reports
# See pyproject.toml coverage for options
coverage-clean:
	rm --force --recursive .coverage
	rm --force --recursive ./htmlcov
	rm --force --recursive coverage.xml

coverage: coverage-clean
	python -m pytest --cov=./iso8583
	python -m coverage html --directory ./htmlcov
	python -m coverage xml -o coverage.xml

coverage-publish: coverage
	codecov -f coverage.xml -t $(TOKEN)

# Generate sphinx docs in docs/_build/html/index.html
docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

# Build and upload release to PyPI
build-clean:
	rm --force --recursive dist/
	rm --force --recursive build/
	rm --force --recursive *.egg-info

build: build-clean
	python ./setup.py sdist bdist_wheel
	python -m twine check dist/*

publish: build
	python -m twine upload dist/*

publish-test: build
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
