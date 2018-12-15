help:
	python3 devsync.py --help

clean:
	rm -rf logs
	coverage erase

.PHONY: test
test:
	python3 testrunner.py

coverage:
	coverage run --source='devsync' testrunner.py
	coverage report

html_coverage: coverage
	coverage html

xml_coverage: coverage
	coverage xml

install:
	sudo pip3 install -r requirements.txt
