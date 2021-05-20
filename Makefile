file_finder = find . -type f $(1) -not -path './venv/*'

PY_FILES = $(call file_finder,-name "*.py")

help:
	python3 devsync.py --help

clean:
	rm -rf logs
	coverage erase

.PHONY: test
test:
	python3 -m unittest

coverage:
	coverage run --source='devsync' python3 -m unittest
	coverage report

html_coverage: coverage
	coverage html

xml_coverage: coverage
	coverage xml

install:
	pip3 install -r requirements.txt

check: check_format flake8

format:
	$(PY_FILES) | xargs black

check_format:
	$(PY_FILES) | xargs black --diff --check

flake8:
	$(PY_FILES) | xargs flake8
