.PHONY: install lint test build-local-api run-local-api build-docker-api start-db migrate build-api start-api create-venv activate-venv 
# create-venv:
# 	python -m venv venv
# 	@echo "Virtual environment created. To activate, run 'venv\Scripts\activate' on Windows."
# activate-venv:
# 	venv\Scripts\activate
build-local-api:
	@echo "Building local API..."
# 	python -m venv venv
# 	venv\Scripts\activate
	python -m pip install --upgrade pip
	pip install --no-cache-dir -r requirements.dev.txt
	@echo "Local API build done..."
run-local-api:
	@echo "Running local API..."
# 	venv\Scripts\activate
	python run.py
	@echo "Local API is running..."
build-docker-api:
	@echo "Building Docker API..."
	docker build -t backend:1.0.0 .
	@echo "Docker API build done..."
start-db:
	docker compose up -d db
migrate:
	docker compose run --rm migrate
build-api:
	docker compose build backend
start-api: build-api
	docker compose up -d backend
test:
	pytest -v --cov=app --cov-report=term-missing
lint:
	flake8 app tests run.py
	-pylint app tests run.py