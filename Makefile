# .PHONY: run install lint test build-local-api run-local-api build-docker-api start-db migrate build-api start-api create-venv activate-venv 
# # create-venv:
# # 	python -m venv venv
# # 	@echo "Virtual environment created. To activate, run 'venv\Scripts\activate' on Windows."
# # activate-venv:
# # 	venv\Scripts\activate

# build:
# 	@echo "Building local API..."
# 	python -m pip install --upgrade pip
# 	pip install --no-cache-dir -r requirements.dev.txt
# 	@echo "Local API build done..."
# migrate:
#     @echo "Checking for migration message..."
# 	@if [ -z "$(M)" ]; then \
# 		read -p "Enter a migration message: " MESSAGE; \
# 		flask db migrate -m "$$MESSAGE"; \
# 	else \
# 		flask db migrate -m "$(M)"; \
# 	fi
# 	this is not working ..
# upgrade:
# 	flask db upgrade
# run:
# 	@echo "Running the application..."
# 	python run.py
# run-gunicorn:
# 	@echo "Starting API using Gunicorn..."
# 	gunicorn -w 2 -b 0.0.0.0:5000 run:app
# test:
# 	pytest -v --cov=app --cov-report=term-missing
# lint:
# 	flake8 app tests run.py
# 	-pylint app tests run.py

# build-docker-api:
# 	@echo "Building Docker API..."
# 	docker build -t backend:1.0.0 .
# 	@echo "Docker API build done..."
# start-db:
# 	docker compose up -d db
# migrate:
# 	docker compose run --rm migrate
# build-api:
# 	docker compose build backend
# start-api: build-api
# 	docker compose up -d backend














# Global configuration

APP_NAME        := backend
IMAGE_NAME      := backend
IMAGE_TAG       ?= 1.0.0
COMPOSE_FILE    := docker-compose.yml
ENV_FILE        := .env

PYTHON          := python
PIP             := pip
FLASK           := flask

BAREMETAL_COMPOSE = docker-compose.baremetal.yml  
#once check the above env 

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
	ci-build ci-test ci-lint ci-docker


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
	@echo "  ci-*               Targets used by CI pipeline"


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


# Migrations (Flask + DB)

migrate-init:
	@echo "Initializing migrations (run once)..."
	$(FLASK) db init

migrate-create:
	@if [ -z "$(M)" ]; then \
		echo "❌ Migration message missing. Use: make migrate-create M=\"message\""; \
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

# -----------------------------
# Docker Compose (full stack)
# -----------------------------
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

# -----------------------------
# CI targets (used by GitHub Actions)
# -----------------------------
ci-build:
	@echo "CI: Build API"
	make build

ci-test:
	@echo "CI: Run tests"
	make test

ci-lint:
	@echo "CI: Run linting"
	make lint

ci-docker:
	@echo "CI: Build Docker image"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

deploy-baremetal:
	@echo "Deploying full stack (Nginx + 2 APIs + DB)..."
	docker compose -f $(BAREMETAL_COMPOSE) up -d --build

destroy-baremetal:
	@echo "Stopping baremetal deployment..."
	docker compose -f $(BAREMETAL_COMPOSE) down