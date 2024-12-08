.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	streamlit run app.py

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete