# =============================================================================
# DEVELOPER EXPERIENCE: MAKEFILE
# =============================================================================
.PHONY: install lint test run docker-build docker-up clean

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

lint:
	@echo "Running static analysis and type checking..."
	ruff check .
	mypy main.py

test:
	@echo "Running evaluation suite..."
	pytest tests/ --cov=main

run:
	@echo "Starting local Uvicorn server..."
	python main.py

docker-build:
	@echo "Building multi-stage optimized Docker image..."
	docker build -t fastapi-ml-optimized:latest .

docker-up:
	@echo "Spinning up standard Compose cluster..."
	docker compose up -d --build

clean:
	@echo "Cleaning up python cache and test artifacts..."
	rm -rf __pycache__ .pytest_cache .ruff_cache .coverage
	docker compose down -v
