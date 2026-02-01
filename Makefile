help:
	python3 devsync.py --help

clean:
	rm -rf logs
	coverage erase

coverage:
	pytest --cov=devsync --cov-report=term-missing --cov-report=xml --cov-report=html tests/
