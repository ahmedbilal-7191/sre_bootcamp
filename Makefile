# Global configuration

APP_NAME := backend
IMAGE_NAME := backend
IMAGE_TAG ?= 1.0.0
COMPOSE_FILE := docker-compose.yml
ENV_FILE := .env

PYTHON := python
PIP := pip
FLASK := flask

BAREMETAL_COMPOSE := docker-compose.baremetal.yml  
# once check the above env 

# Export env vars from .env if present
ifneq (,$(wildcard $(ENV_FILE)))
	include $(ENV_FILE)
	export
endif

.PHONY: help \
	install build test lint run run-gunicorn \
	db-up db-down db-status \
	migrate-init migrate-create migrate-upgrade \
	docker-build docker-run \
	compose-build compose-up compose-down \
	deploy-baremetal destroy-baremetal


# Help

help:
	@echo "Available targets:"
	@echo "  install            Install local dependencies"
	@echo "  build              Prepare local build (deps)"
	@echo "  test               Run unit tests"
	@echo "  lint               Run linting"
	@echo "  run                Run app locally (dev)"
	@echo "  run-gunicorn       Run app using Gunicorn"
	@echo ""
	@echo "  db-up              Start database container"
	@echo "  db-down            Stop database container"
	@echo "  db-status          Show database container status"
	@echo ""
	@echo "  migrate-init       Initialize migrations folder (run once)"
	@echo "  migrate-create     Create a new migration (M=\"message\")"
	@echo "  migrate-upgrade    Apply migrations to DB"
	@echo ""
	@echo "  docker-build       Build API Docker image"
	@echo "  docker-run         Run API Docker container"
	@echo ""
	@echo "  compose-build      Build services using docker-compose"
	@echo "  compose-up         Start DB, run migrations, start API"
	@echo "  compose-down       Stop all services"
	@echo ""
	@echo "  deploy-baremetal   Deploy full stack (Nginx + 2 APIs + DB)"
	@echo "  destroy-baremetal  Stop baremetal deployment"


# Local development

install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install --no-cache-dir -r requirements.dev.txt

build: install
	@echo "Local build completed."

run:
	@echo "Running API locally..."
	$(PYTHON) run.py

run-gunicorn:
	@echo "Running API with Gunicorn..."
	gunicorn -w 2 -b 0.0.0.0:5000 run:app

test:
	@echo "Running tests..."
	pytest -v --cov=app --cov-report=term-missing

lint:
	@echo "Running linters..."
	flake8 app tests run.py
	-pylint app tests run.py

# pylint app tests run.py || true

# Database (Docker)

db-up:
	@echo "Starting database..."
	docker compose up -d db

db-down:
	@echo "Stopping database..."
	docker compose stop db

db-status:
	docker compose ps db

db-migrate:
	@echo "Running database migrations using Docker Compose..."
	docker compose run --rm migrate

# Migrations (Flask + DB)

migrate-init:
	@echo "Initializing migrations (run once)..."
	$(FLASK) db init

migrate-create:
	@if [ -z "$(M)" ]; then \
		echo "Migration message missing. Use: make migrate-create M=\"message\""; \
		exit 1; \
	fi
	@echo "Creating migration: $(M)"
	$(FLASK) db migrate -m "$(M)"

migrate-upgrade:
	@echo "Applying migrations..."
	$(FLASK) db upgrade


# Docker (single container)

docker-build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run:
	@echo "Running Docker container..."
	docker run --env-file $(ENV_FILE) -p 5000:5000 $(IMAGE_NAME):$(IMAGE_TAG)


# Docker Compose (full stack)

compose-build:
	@echo "Building services..."
	docker compose build

compose-up:
	@echo "Starting DB..."
	docker compose up -d db
	@echo "Running migrations..."
	docker compose run --rm migrate
	@echo "Starting API..."
	docker compose up -d backend

compose-down:
	@echo "Stopping all services..."
	docker compose down



deploy-baremetal:
	@echo "Deploying full stack (Nginx + 2 APIs + DB)..."
	docker compose -f $(BAREMETAL_COMPOSE) up -d --build

destroy-baremetal:
	@echo "Stopping baremetal deployment..."
	docker compose -f $(BAREMETAL_COMPOSE) down
	