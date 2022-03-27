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
	coverage run --source='devsync' -m unittest
	coverage report

html_coverage: coverage
	coverage html

xml_coverage: coverage
	coverage xml

install:
	pip3 install -U -r requirements.txt
