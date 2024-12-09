IMAGE_NAME = review-analyzer

.PHONY: install test format lint clean run docker-build docker-run all

# Development Setup
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Testing and Code Quality
test:
	python -m pytest tests/ --cov=services

format:
	black .
	isort .

lint:
	ruff check .

# Cleaning
clean:
	rm -rf .pytest_cache .coverage .pytest_cache __pycache__ .ruff_cache
	rm -rf **/__pycache__
	rm -rf **/*.pyc

# Local Development (run in separate terminals)
run-api:
	uvicorn api:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	streamlit run app.py

# Docker Commands
image-show:
	docker images

container-show:
	docker ps

docker-build:
	docker build -t review-analyzer .

docker-run:
	docker run -p 8000:8000 -p 8501:8501 -v $(PWD)/.streamlit:/app/.streamlit review-analyzer

docker-stop:
	docker ps -q | xargs -r docker stop
	docker ps -aq | xargs -r docker rm

docker-clean:
	@echo "==> Stopping containers..."
	-docker stop $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME))
	@echo "==> Removing containers..."
	-docker rm -f $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME))
	@echo "==> Removing image..."
	-docker rmi -f $(IMAGE_NAME)
	@echo "==> Clean complete"

# Combined Commands
all: install format lint test

# Run all services (for documentation purposes)
run:
	@echo "Please run the services in separate terminals:"
	@echo "Terminal 1: make run-api"
	@echo "Terminal 2: make run-frontend"