.PHONY: help install test lint format clean docker-build docker-up docker-down migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up   - Start Docker services"
	@echo "  docker-down - Stop Docker services"
	@echo "  migrate     - Run database migrations"
	@echo "  dev         - Start development server"
	@echo "  prod        - Start production server"

# Installation
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Testing
test:
	pytest -v

test-coverage:
	pytest --cov=app --cov-report=html

test-fast:
	pytest -q

# Code quality
lint:
	black --check app/ tests/
	ruff check app/ tests/

format:
	black app/ tests/
	ruff format app/ tests/

# Cleanup
clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.pytest_cache" -exec rm -rf {} +
	find . -type f -name "test.sqlite" -delete
	rm -rf htmlcov/

# Docker commands
docker-build:
	docker build -t l10nlight:latest .

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Database
migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(MSG)"

reset-db:
	docker-compose down -v
	docker-compose up db --build

# Development
dev:
	python -m app.server

dev-docker:
	docker-compose -f docker-compose.dev.yaml up --build

# Production
prod:
	docker-compose up -d

# Utilities
shell:
	docker-compose exec api bash

db-shell:
	docker-compose exec db psql -U app -d app

check-deps:
	safety check
	pip-audit
