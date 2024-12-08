.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete