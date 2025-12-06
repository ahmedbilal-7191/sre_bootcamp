## SRE Bootcamp – From Local to Production (Student CRUD REST API)

This repository is part of the SRE Bootcamp – Part One: From Local to Production, where we build, containerize, deploy, and observe a production-grade microservice.
The journey begins by developing a simple REST API and evolves step-by-step into a fully automated and observable production deployment using:

Containers

CI/CD pipelines

Bare-metal deployments

Kubernetes

Helm Charts

GitOps with ArgoCD

Observability stack (Prometheus, Loki, Grafana, Alertmanager)

Dashboards & Alerts

The goal is to learn real-world SRE workflows by building everything from scratch.

Features are above or add some more

📦 Tech Stack
Component	Technology
Language	Python 3
Framework	Flask
ORM	SQLAlchemy
DB	PostgreSQL
Migrations	Flask-Migrate
Validation	Marshmallow
Logging	python-json-logger
Metrics	prometheus-client (used in later stages)
WSGI Server	gunicorn
Testing	pytest, pytest-flask
Linting	pylint, flake8

------------------------------------------------------------------------------------------------------------------ 

## Milesstone - 1

Quick Start:

Prerequisites:
1.python to run the application 
2.postgresql DB


Local Setup Instructions:

1. Clone the repository
git clone https://github.com/<your-username>/sre-bootcamp-students-api.git
cd sre-bootcamp-students-api


2.Create local .env by copying:

cp .env.example .env

3. Create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows	

Step 3 — Install Dependencies

Instead of manually installing dependencies using pip install,
you can simply run the Make target:

make build-local-api

Runs:
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.dev.txt

5. Run migrations

make migrate

Runs:
flask db init
flask db migrate
flask db upgrade

6. Start the API
Option A — Flask Dev Server

make run

Runs:

python run.py

Option B — Gunicorn (production style)

make run-gunicorn:

Runs:
gunicorn --bind 0.0.0.0:8000 "app:create_app()"

🧰 Makefile Commands
Command	Description
make run	Start Flask API
make run-gunicorn Start Gunicorn server for API
make test	Run test suite
make migrate	Generate migration
make upgrade	Apply migrations
make lint	Run flake8 & pylint



📁 Project Structure
.
├── .github/
│   └── workflows/              # CI/CD workflow definitions (GitHub Actions)
│
├── app/
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── student.py
│   │
│   ├── routes/                 # API route handlers
│   │   ├── __init__.py
│   │   └── student_routes.py
│   │
│   ├── schemas/                # Marshmallow schemas for validation/serialization
│   │   ├── __init__.py
│   │   └── student_schema.py
│   │
│   ├── services/               # Service layer / business logic
│   │   ├── __init__.py
│   │   └── student_service.py
│   │
│   ├── utils/                  # Utility modules
│   │   ├── __init__.py
│   │   ├── custom_errors.py
│   │   ├── error_helpers.py
│   │   ├── helpers.py
│   │
│   ├── errors.py               # Centralized error handlers
│   ├── extensions.py           # DB, Marshmallow, JWT, Logger initialization
│   ├── logging_config.py       # Logging configuration
│
│   ├── __init__.py             # Flask application factory
│
├── migrations/                 # Alembic migrations
│
├── tests/                      # Unit tests
│
├── .env.example                # Example environment variables template
├── .gitignore
├── Makefile                    # Make targets for build, linting, testing, docker, etc.
├── README.md                   # Project documentation
├── config.py                   # App configuration (dev/prod/test)
├── gunicorn.conf.py            # Gunicorn production config
├── requirements.dev.txt        # Development dependencies (flake8, pytest, black)
├── requirements.txt            # Production dependencies
└── run.py                      # Entry point (Flask dev server)

This structure supports clean separation of concerns and scales well as we later introduce Docker, CI/CD, K8s, Helm, and Observability.

Architecture Overview:This project is a modular and scalable REST API Web Server built using Flask, following clean architecture principles.
The system is organized into clear layers that separate responsibilities, making the codebase maintainable, testable, and extensible.

          ┌──────────────────────────────┐
          │          Client / UI         │
          │  (Postman, curl, frontend)   │
          └───────────────┬──────────────┘
                          │ HTTP Requests
                          ▼
           ┌──────────────────────────────────┐
           │        Flask REST API            │
           │            (run.py)              │
           └─────────────────┬────────────────┘
                             │ Routes (API Layer)
                             ▼
         ┌────────────────────────────────────────┐
         │            Routes Layer                │
         │   app/routes/student_routes.py         │
         │ - Defines API versioning (/api/v1)     │
         │ - Maps HTTP methods → controller logic │
         └─────────────────┬──────────────────────┘
                           │ Calls
                           ▼
         ┌────────────────────────────────────────┐
         │          Service Layer                 │
         │    app/services/student_service.py     │
         │ - Business logic                       │
         │ - DB operations via SQLAlchemy         │
         │ - Validation orchestration             │
         └─────────────────┬──────────────────────┘
                           │ Uses Models
                           ▼
         ┌────────────────────────────────────────┐
         │               Data Layer               │
         │            app/models/student.py       │
         │ - SQLAlchemy ORM Model                 │
         │ - Handles persistence                  │
         └─────────────────┬──────────────────────┘
                           │
                           ▼
         ┌────────────────────────────────────────┐
         │            PostgreSQL / SQLite         │
         │         (via SQLAlchemy ORM)           │
         └────────────────────────────────────────┘


🗄️ Database Table: students

The REST API stores student records in a SQL database using SQLAlchemy ORM.

The table is created using the following model:

📌 Students Table Schema
| Column       | Type        | Constraints                         | Description                        |
| ------------ | ----------- | ----------------------------------- | ---------------------------------- |
| `id`         | Integer     | Primary Key, Auto-increment         | Unique identifier for each student |
| `name`       | String(100) | Required, Cannot contain digits     | Student’s full name                |
| `age`        | Integer     | Required, Range(5–100)              | Student’s age                      |
| `grade`      | String(20)  | Required                            | Class or grade of the student      |
| `email`      | String(120) | Required, Unique, Valid email       | Student’s email address            |
| `created_at` | DateTime    | Default = timestamp at row creation | When the record was created        |
| `updated_at` | DateTime    | Auto-updated on modification        | When the record was last updated   |


The API supports the following operations:

🚀 Supported API Endpoints (v1)

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| POST   | `/api/v1/students`      | Create a new student    |
| GET    | `/api/v1/students`      | Get all students        |
| GET    | `/api/v1/students/<id>` | Get a student by ID     |
| PUT    | `/api/v1/students/<id>` | Update a student record |
| DELETE | `/api/v1/students/<id>` | Delete a student record |
| GET    | `/healthcheck`          | Health check endpoint   |


📬 Postman Collection

Import postman_collection.json to test the API.


Example Request:

Example Response:



⚙️ Environment Configuration

All configuration is passed through environment variables, following 12-Factor App standards.

Below is the list of environment variables used by the application:

| Variable Name       | Description                                | Example Value |
| ------------------- | ------------------------------------------ | ------------- |
| `FLASK_ENV`         | Flask environment mode                     | `development` |
| `POSTGRES_USER`     | PostgreSQL username                        | `db_user`     |
| `POSTGRES_PASSWORD` | PostgreSQL password                        | `db_password` |
| `POSTGRES_DB`       | Name of the database                       | `db_name`     |
| `POSTGRES_HOST`     | Database host (service name in Docker/K8s) | `db_host`     |
| `POSTGRES_PORT`     | Port for PostgreSQL                        | `5432`        |
| `LOG_LEVEL`         | Application logging level                  | `INFO`        |



🧪 Testing

Run tests:

pytest --cov=app


Tests include:

Healthcheck
CRUD endpoints
Input validation
DB interactions


🧾 Logging

All logs use JSON format:

{
  "timestamp": "2025-01-10T12:45:20Z",
  "level": "INFO",
  "logger":svcname,
  "message": "Student created",
  "log_type": "application"
}

------------------------------------------------------------------------

🚀 Milestone 2 – Dockerization & Image Optimization

This milestone focuses on running the API using Docker, creating a multi-stage Dockerfile, injecting environment variables at runtime, optimizing image size, and tagging images using semantic versioning (semver).

🐳 Docker Usage Instructions
Build Docker Image
Without Makefile:
docker build -t my-api:1.0.0 .

With Makefile:
make docker-build VERSION=1.0.0

Run the API Container
Without Makefile:
docker run -p 5000:5000 \
  -e DB_HOST=localhost \
  -e DB_USER=root \
  -e DB_PASS=password \
  my-api:1.0.0

With Makefile:
make docker-run VERSION=1.0.0

🧪 Environment Variables

The following environment variables can be injected at runtime:

Variable	Description
DB_HOST	Database hostname
DB_USER	DB username
DB_PASS	DB password
PORT	Application port

📦 Makefile Targets Added
docker-build:
    docker build -t my-api:$(VERSION) .

docker-run:
    docker run -p 8080:8080 --env-file .env my-api:$(VERSION)

docker-push:
    docker push my-api:$(VERSION)

🪶 Docker Image Optimization Techniques Used

Multi-stage builds

Lightweight base (alpine or slim)

Removed unnecessary dependencies

Cached layers

Smaller final runtime layer

---------------------------------------------------------
🚀 Milestone 3 – One-Click Local Development Setup

This milestone focuses on making local development extremely simple for any team member—even if they do not already have the required tools installed. Using Docker Compose, Makefile automation, and helper scripts, the entire stack (API + Database + Migrations) can now be started with a single command.

2. Makefile Targets Added

The Makefile now includes targets to automate:

Target	Description
make db-start	Starts the DB service
make db-migrate	Runs DB DML migrations
make docker-build	Builds the REST API Docker image
make api-start	Starts API (DB + migrations + API container)
make setup-tools (optional)	Installs required tools using bash functions


🛠️ Pre-Requisites

Before running the project, ensure the following tools are installed:

1. Docker

Check installation:

docker --version

2. Docker Compose

(Check included in Docker Desktop)

docker compose version

3. Make
make --version

🚀 One-Click Local Development Setup

The goal is to allow any team member to run the API with a single command.

🧰 Step-by-Step Local Setup
1️⃣ Start the Database
make db-start


This will:

Start DB container

Create network if needed

2️⃣ Run Database DML Migrations
make db-migrate


This will:

Check whether DB is reachable

Apply all DML migrations

3️⃣ Build the API Docker Image
make docker-build VERSION=1.0.0


Uses semantic versioning.

4️⃣ Start the REST API
make api-start VERSION=1.0.0


This command automatically:

Starts the DB (if not already running)

Applies migrations

Builds the API Docker image (optional, if missing)

Starts the API using docker compose up

This ensures the entire stack is started in the correct order without any manual steps.

🐳 Docker Compose Overview

The docker-compose.yml includes:

database service

api service

Shared network

Environment variables

Dependencies (depends_on)

This guarantees that the API waits until DB is available.

📝 Makefile Overview

Example targets included (your actual Makefile may differ):

db-start:
    docker compose up -d db

db-migrate:
    docker exec db-container-name python migrate.py

docker-build:
    docker build -t my-api:$(VERSION) .

api-start:
    make db-start
    make db-migrate
    docker compose up -d api

do the migration -m required by using the image and run the commad directly by migrate:
	docker compose run --rm backend flask db migrate
	docker compose run --rm backend flask db upgrade seperated or single 
	
-------------------------------------------

🚀 Milestone 4 – Continuous Integration (CI) Pipeline Setup

This milestone introduces a fully automated CI pipeline powered by GitHub Actions and executed on a self-hosted runner.
The goal is to ensure code quality, automated builds, testing, linting, and Docker image publishing — all triggered only when relevant code changes occur.

The CI workflow includes the following stages, executed in the order listed:

1. Build API

The API is built using a dedicated Makefile target (e.g., make build).
This guarantees consistent build steps across local and CI environments.

2. Run Tests

Unit and integration tests are executed using a Makefile target (e.g., make test).
This ensures code correctness before producing a Docker image.

3. Perform Code Linting

Linting is performed via a Makefile target (e.g., make lint) using tools such as flake8.
This helps maintain code quality and enforce styling guidelines.

4. Docker Login

The pipeline authenticates to Docker Hub using GitHub Secrets:

DOCKER_USERNAME

DOCKER_PASSWORD

Authentication is required before pushing Docker images.

5. Docker Build and Push

A Docker image is built and pushed to Docker Hub using either:

Makefile Docker targets, or

GitHub’s official Docker actions

Images may follow semantic versioning (SemVer), depending on your repository structure.

🧱 Makefile Integration

All core pipeline actions—build, test, and lint—are executed using Makefile targets.
This ensures:

Identical commands locally and in CI

Cleaner workflow YAML

Easier to reproduce and debug builds

Example targets (conceptual):

build:
    # Build API code

test:
    # Run automated tests

lint:
    # Perform code linting

docker-build:
    # Build Docker image

docker-push:
    # Push Docker image


The CI pipeline simply calls these targets instead of duplicating logic.

🖥️ Self-Hosted GitHub Runner (Local Machine)

This pipeline is executed on a self-hosted runner installed on your local system.
This runner is responsible for:

Running Makefile commands

Building Docker images

Authenticating and pushing to Docker Hub

Since Docker build and push are part of the pipeline, the self-hosted runner must have:

Docker Engine

Docker CLI

Make

Python (optional, depending on your app)

The workflow uses:

runs-on: self-hosted


This ensures all CI tasks run locally instead of using GitHub-hosted runners.

🎯 Trigger Rules

The CI pipeline is designed to run only when relevant changes occur.

✔ Trigger on code changes only

The workflow executes only when files inside the code/ directory are modified:

on:
  push:
    paths:
      - "code/**"


This prevents unnecessary pipeline runs from changes to docs, configs, or unrelated directories.

✔ Manual Trigger Enabled

The workflow can also be started manually from the GitHub Actions UI:

Actions → CI Pipeline → Run Workflow


Enabled using:

workflow_dispatch:


This allows developers to run the CI pipeline on demand, even without pushing code.


📌 Milestone 5 — Deploy REST API & Dependent Services on Bare Metal

This milestone focuses on deploying the REST API and all supporting services on a bare-metal environment using Vagrant, Bash provisioning, Docker Compose, and Nginx load balancing.

The end goal is to create a fully functional multi-container environment that exposes the API through a load balancer and verifies that the service is operational.

🚀 Deployment Overview

The deployment uses:

Vagrant → to provision a bare-metal VM

Bash script → to configure the VM and install dependencies

Docker Compose → to orchestrate all containers

Makefile → to simplify deployment commands

Nginx → to load balance traffic between API replicas

🔧 Infrastructure Provisioning
✔ Vagrant Setup

A Vagrantfile is used to:

Spin up a VM

Allocate CPU, memory, and networking configurations

Set up a synced folder (if required)

Call a provisioning bash script

Example concepts included:

config.vm.box = "ubuntu/focal64"
config.vm.provision "shell", path: "bootstrap.sh"

✔ Bash Script Provisioning

The VM is configured using a bootstrap.sh or similar script that includes:

Modular bash functions for installation tasks

Installation of required packages such as:

Docker

Docker Compose

Git

curl / wget

Python (if needed)

Adding the vagrant user to the Docker group

System updates and service setup

This ensures idempotent, repeatable VM provisioning.

🐳 Application Deployment Using Docker Compose

The deployment uses docker-compose.yaml to orchestrate:

🔹 2 API containers

Running the REST API application, scaled using:

deploy:
  replicas: 2


or using explicit services:

api-1

api-2

🔹 1 Database container

A single DB instance such as PostgreSQL or MySQL.

🔹 1 Nginx container

Configured as a load balancer in front of the two API replicas.

The final setup runs 4 containers:

Service	Purpose
API-1	REST API instance
API-2	REST API instance
DB	Database
Nginx	Load balancer
⚙️ Makefile Integration

A Makefile is included in the repository to simplify deployment tasks such as:

setup:
	docker-compose pull

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f


This ensures a consistent way to run, stop, and monitor the environment across local and VM environments.

🌐 Nginx Load Balancing

The Nginx configuration must be committed to the GitHub repository, including:

nginx.conf

Dockerfile (if customizing)

Compose references

Nginx performs round-robin load balancing across the two API containers.

Example upstream block (conceptual):

upstream api_backend {
    server api-1:5000;
    server api-2:5000;
}

External Access

Users access the API through port 8080 on the host / VM.

Nginx forwards requests internally to API containers:

api-1:5000

api-2:5000

🔍 Functional Validation

After deployment:

✔ API must be accessible via:
http://<vm-ip>:8080

✔ Nginx should distribute traffic across both API containers.
✔ All API endpoints must return HTTP 200 OK when tested using Postman.

This confirms that:

The API is running

Load balancing works correctly

Containers are healthy

Database connectivity is functional

📁 Repository Requirements

The following files must be included in the repository:

Vagrantfile

Provisioning bash script (e.g., bootstrap.sh)

docker-compose.yaml

Makefile

Nginx config (nginx.conf)

Any additional environment or service configs



-------------------
📌 Milestone 6 — Setup Kubernetes Cluster

This milestone focuses on creating a multi-node Kubernetes cluster using Minikube and preparing it for future production-like deployments.
The cluster will be used to run the application, database, and dependent services in isolated node groups, similar to a real production topology.

1️⃣ Spin Up a Multi-Node Minikube Cluster

A four-node cluster must be created:

1 control-plane node

3 worker nodes

Example:

minikube start --nodes 4 -p prod-cluster

2️⃣ Label the Worker Nodes Appropriately

Add labels to instruct the scheduler where to run future workloads:

Worker Node	Label
Node A	type=application
Node B	type=database
Node C	type=dependent_services

Example:

kubectl label node prod-cluster-m02 type=application
kubectl label node prod-cluster-m03 type=database
kubectl label node prod-cluster-m04 type=dependent_services


These labels will later be used in Deployment manifests:

nodeSelector:
  type: application

3️⃣ Enable CSI HostPath Storage Driver

To support multi-node storage provisioning, enable Minikube’s CSI hostpath addon:

minikube addons enable csi-hostpath-driver -p prod-cluster


This provides a CSI-driven dynamic storage backend.

4️⃣ Update the Default Storage Class

Minikube creates a default storage class that does not support multi-node scheduling.
We must:

✔ Mark the CSI HostPath StorageClass as default
✔ Ensure future PVCs bind to volumes that stay on the correctly labeled node

Steps:

Edit the CSI storage class:

kubectl edit storageclass csi-hostpath-sc


Ensure it includes:

metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"


(Optional but recommended) Remove default annotation from the old storage class:

kubectl patch storageclass standard -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'


This ensures:

All PVCs use CSI HostPath

PVs are provisioned on the same node where the pod is scheduled

Ideal for future DB/stateful components

🧪 Why CSI HostPath Matters

Normal Minikube storage works only for single-node clusters.
With CSI HostPath:

Each worker node has its own CSI driver mount

Volumes are provisioned per node

This perfectly pairs with your node labels:

For example:

Database Pods → Node B → Volumes also on Node B

Application Pods → Node A → Volumes on Node A

This prevents cross-node storage issues.
------------------------------------
Milestone 7 – Deploy REST API & Dependent Services in Kubernetes
✅ Objective

In this milestone, we migrate from bare-metal Vagrant deployments to Kubernetes-based deployments.
Your REST API, database, and supporting components are now deployed on the 3-node Minikube cluster created in the previous milestone.

This milestone teaches:

Creating and modifying Kubernetes manifests

Using ConfigMaps, Secrets, and External Secrets Operator

Node labeling & scheduling

Understanding Kubernetes service types

Integrating HashiCorp Vault with ESO


🚀 Deployment Architecture
Node	Label	Usage
Node A	type=application	REST API deployment
Node B	type=database	PostgreSQL DB
Node C	type=dependent_services	Vault, ESO, Observability stack

You previously configured node labels using:

kubectl label node <node-name> type=application
kubectl label node <node-name> type=database
kubectl label node <node-name> type=dependent_services


All YAML manifests ensure workloads are scheduled correctly using:

nodeSelector:
  type: application   # or database, dependent_services

🔐 Secrets Management with ESO + Vault
1. Vault runs inside Kubernetes (Node C)

Vault stores:

DB username

DB password

API secrets

2. External Secrets Operator (ESO) pulls secrets from Vault

We declare a SecretStore pointing to Vault:

apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: student-api
spec:
  provider:
    vault:
      server: "http://vault.vault:8200"
      path: "student-api/"
      version: "v2"
      auth:
        token:
          name: vault-token
          key: token

3. Application and DB use ExternalSecret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: student-api
spec:
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: db-secret
  data:
    - secretKey: username
      remoteRef:
        key: db-user
    - secretKey: password
      remoteRef:
        key: db-pass


This auto-creates:

db-secret


Used by application and DB.

🗃️ Database Deployment with Init Container (DML Migrations)

DB migrations must run before application pod starts.

Your application.yml includes:

initContainers:
  - name: run-migrations
    image: my-api:latest
    command: ["sh", "-c", "python manage.py run_migrations"]
    envFrom:
      - secretRef:
          name: db-secret


The migration init container ensures DB is ready before the main app container starts.

📦 Storage Class (CSI HostPath)

You enabled and modified:

minikube addons enable csi-hostpath-driver


Then edited default storage class:

volumeBindingMode: WaitForFirstConsumer


This ensures PV is created on the correct node where the pod is scheduled, crucial for multi-node Minikube.

📡 Exposing REST API

The REST API is exposed via Kubernetes Service:

apiVersion: v1
kind: Service
metadata:
  name: student-api-service
spec:
  type: NodePort
  selector:
    app: student-api
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 32000


You can access API at:

http://<minikube-ip>:32000

🧪 Validate API

Using Postman:

GET /students → 200 OK

POST /students → 200 OK

PUT /students/:id → 200 OK

DELETE /students/:id → 200 OK

Ensure databases are functioning and init-migrations ran successfully.

📜 Steps to Deploy Everything
1. Start 3-node Minikube

(Already completed)

2. Apply namespaces
kubectl apply -f k8s/namespaces/

3. Deploy Vault
kubectl apply -f k8s/vault/

4. Deploy ESO + SecretStore
kubectl apply -f k8s/eso/

5. Deploy Database (Node B)
kubectl apply -f k8s/database/database.yml

6. Deploy Application (Node A)
kubectl apply -f k8s/application/application.yml

7. Verify Services
kubectl get pods -A
kubectl get svc -A

8. Test API
http://<minikube-ip>:32000/health




---------------------------
Milestone 8 – Deploy REST API & Dependent Services Using Helm Charts
🎯 Objective

In this milestone, we transition from raw Kubernetes manifests to Helm-based deployments for the REST API, database, Vault, and other dependent services.
Helm allows us to package, version, parameterize, and reuse deployments in a clean and production-friendly manner.

This milestone teaches:

Helm chart structure (templates, values, helpers)

Best practices for chart packaging

Using subcharts and dependency management

Deploying all services using Helm instead of raw YAML





Helm Best Practices Followed
✔ Templates split into reusable helper files

_helpers.tpl contains:

labels

annotations

naming conventions (e.g., {{ include "student-api.fullname" . }})

✔ No hardcoded values

Everything configurable is in values.yaml:

image

resources

nodeSelector

Vault secret paths

DB connection URLs

Service type (NodePort / ClusterIP)

✔ Node scheduling handled through values

Example in values.yaml:

nodeSelector:
  type: application


Overridden for other charts like:

nodeSelector:
  type: database

✔ ESO + Vault integration parameterized

ExternalSecret template uses values like:

vault:
  path: "student-api/"
  secretKeys:
    username: db-user
    password: db-pass

✔ DB migrations handled via Helm hooks or initContainers

Your API Helm chart includes:

initContainers:
  - name: run-migrations
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    command: ["sh", "-c", "python manage.py run_migrations"]

🚀 Deployment Workflow Using Helm
1. Add dependency charts (optional)

If using community charts:

helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add external-secrets https://charts.external-secrets.io


For local copies (recommended), they are already inside helm/.

📦 Install Each Component
1. Create namespaces via Helm

Student API chart includes namespace.yaml inside templates, so installation handles it automatically.

2. Deploy Vault (Node C)
helm install vault helm/vault -n vault

3. Deploy External Secrets Operator
helm install eso helm/eso -n external-secrets

4. Deploy Database (Node B)

If using your custom chart:

helm install student-db helm/database -n student-api


If using community chart inside repo:

helm install student-db helm/database -n student-api


Both work because chart is bundled.

5. Deploy REST API (Node A)
helm install student-api helm/student-api -n student-api


Values can be overridden:

helm install student-api helm/student-api \
  --namespace student-api \
  -f helm/student-api/values-prod.yaml

📡 Access the REST API

If using NodePort:

kubectl get svc -n student-api


Example URL:

http://<minikube-ip>:32000


You can test using Postman:

GET /students → 200

POST /students → 200

🔐 Secret Flow Recap (Helm Version)

Vault stores DB credentials

ESO chart deploys ExternalSecret + SecretStore

Helm renders ExternalSecret YAML for API and DB

ESO converts Vault secrets → K8s secrets

Pods mount secrets via environment variables

Everything is controlled via values:

vault:
  secretStoreName: vault-backend
  secretPath: "student-api/"

🔄 Updating Deployments (Helm Upgrade)
helm upgrade student-api helm/student-api -n student-api


--------------------------------------------------------
Milestone 9 — Setup One-Click Deployments Using ArgoCD
🎯 Objective

This milestone introduces GitOps-based automated deployments using ArgoCD.
Instead of running kubectl apply or Helm commands manually, ArgoCD continuously monitors your GitHub repository and deploys changes automatically.

This milestone teaches:

GitOps principles

ArgoCD installation & configuration

Declarative ArgoCD Applications

Auto-syncing Helm charts

CI → Git push → ArgoCD auto-deploy pipeline

Updating Helm image tags automatically through GitHub Actions

🧱 ArgoCD Overview

ArgoCD is a GitOps controller that:

Watches your Git repository

Syncs Kubernetes manifests or Helm charts to the cluster

Detects drift and corrects it

Allows continuous deployment without manual intervention

ArgoCD becomes the single source of deployment truth for your Kubernetes cluster.



📁 Repository Layout for GitOps

Your repo now includes:

helm/
  student-api/
  database/
  vault/
  eso/

argocd/
  apps/
    student-api.yaml
    database.yaml
    vault.yaml
  secrets/
    repo-credentials.yaml


✔ Helm charts remain unchanged.
✔ ArgoCD YAML definitions are fully declarative.
✔ No manual creation of ArgoCD resources.

🚀 ArgoCD Installation & Setup
1. Create the Namespace
kubectl create namespace argocd

2. Install ArgoCD Components
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

3. Schedule ArgoCD on the dependent_services Node

Label your node:

kubectl label node <node-name> type=dependent_services


Patch ArgoCD deployments (or set via Helm charts):

spec:
  template:
    spec:
      nodeSelector:
        type: dependent_services


Components deployed:

argocd-server

argocd-repo-server

argocd-application-controller

argocd-dex-server

redis

All under argocd namespace.

📝 Declarative ArgoCD Manifests

No UI clicks.
Everything is written as YAML in the repo.

Example: argocd/apps/student-api.yaml

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: student-api
  namespace: argocd
spec:
  destination:
    namespace: student-api
    server: https://kubernetes.default.svc
  source:
    repoURL: https://github.com/<yourname>/<repo>.git
    path: helm/student-api
    targetRevision: main
    helm:
      valueFiles:
        - values.yaml
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true


✔ Pulls Helm charts directly
✔ Uses repo as source of truth
✔ Auto sync and drift correction enabled

🔐 Repository Access via ArgoCD

ArgoCD requires repository credentials:

argocd/secrets/repo-credentials.yaml:

apiVersion: v1
kind: Secret
metadata:
  name: github-repo-creds
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repo-creds
stringData:
  url: https://github.com/<your-repo>
  username: <github-username>
  password: <github-token>


✔ Committed declaratively
✔ No UI secret creation

🔄 CI Workflow: Update Helm Chart Image Tags

Your GitHub Actions CI pipeline now includes an additional job:

Purpose

After CI succeeds (build → tests → lint → docker push)

Pull the Helm chart from the repo

Update the image tag in values.yaml to the new version

Commit the update

Push to main branch

This enables one-click deployments because ArgoCD automatically detects the update and deploys it.

Sample Workflow Logic
jobs:
  update-helm-image-tag:
    runs-on: self-hosted
    needs: build-test-lint-push

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Update image tag
        run: |
          sed -i "s/tag:.*/tag: $NEW_IMAGE_TAG/" helm/student-api/values.yaml

      - name: Commit changes
        run: |
          git config user.name "CI Bot"
          git config user.email "ci-bot@example.com"
          git commit -am "Update image tag to $NEW_IMAGE_TAG"
          git push


✔ Runs on your self-hosted GitHub runner
✔ ArgoCD detects commit → auto syncs → deployment updated automatically

⚙ Deploying Apps via ArgoCD (One Click)

Once ArgoCD is installed and the Application manifests are applied:

kubectl apply -f argocd/apps/ -n argocd


ArgoCD now:

Pulls your Helm chart

Installs all components

Monitors values.yaml for changes

Syncs automatically on updates

Applies drift correction

Everything is GitOps-driven.

🌐 Access ArgoCD UI (Optional)

Expose port:

kubectl port-forward svc/argocd-server -n argocd 8080:80


Access UI:

http://localhost:8080


Fetch initial password:

kubectl get secret argocd-initial-admin-secret \
  -n argocd -o jsonpath="{.data.password}" | base64 -d





----------------------------------

Milestone 10 — Setup an Observability Stack (Prometheus, Loki, Grafana, Promtail)
🎯 Objective

This milestone focuses on setting up a complete observability stack using:

Prometheus → Metrics

Loki → Logs

Promtail → Log collection

Grafana → Visualization

DB Metrics Exporter → Database monitoring

Blackbox Exporter → Endpoint monitoring

The goal is to achieve full visibility into the REST API, database, Vault, ArgoCD, and all dependent services deployed in the Kubernetes cluster.

📘 Learning Outcomes

By completing this milestone, you will learn:

Concepts of monitoring, logging, and observability

Prometheus metrics collection

Loki log indexing & querying

Promtail log scraping

Grafana dashboards

Exporters for application, DB, and network endpoint monitoring

Configuring Kubernetes node selectors for dedicated observability workloads

🚀 Problem Statement

We need to deploy a complete PLG (Promtail, Loki, Grafana) stack with Prometheus to monitor:

Our REST API

Database

Vault

ArgoCD server

All node-level metrics

Application logs

Endpoint uptime & latency

Kubernetes cluster state

The scope includes:

Deploy all observability workloads on the dependent_services node.

Use Helm charts for all components.

Store all Helm charts/configs in the same GitHub repository in the correct structure.

✔ Expectations & Architecture
🧱 1. Deploy Prometheus, Loki, Grafana on a Dedicated Node

All observability components must run on the dependent_services node in the namespace:

observability


Add node labels such as:

kubectl label node <NODE_NAME> type=dependent_services


Each Helm chart must include:

nodeSelector:
  type: dependent_services


Components deployed:

Prometheus

Loki (TSDB schema)

Grafana

Kube-state-metrics

Node-Exporter

Blackbox Exporter

DB Metrics Exporter

Promtail

📦 2. Promtail → Send Application Logs Only

Promtail must:

Tail logs only from API pods (via label selectors or file paths)

Exclude logs from system pods, exporters, and other infrastructure

Example:

scrape_configs:
  - job_name: student-api-logs
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: student-api
        action: keep


This ensures only app logs go to Loki.

📊 3. Deploy DB Metrics Exporter

Depending on DB type:

PostgreSQL → postgres-exporter

MySQL → mysqld-exporter

Exporter must run inside observability namespace.

Prometheus scrape config example:

- job_name: db-exporter
  static_configs:
    - targets: ['db-exporter.observability.svc:9187']

🌐 4. Deploy Blackbox Exporter (Endpoint Monitoring)

The blackbox exporter monitors:

REST API (/health)

ArgoCD server

Hashicorp Vault

DB endpoint (optional ping)

Any internal service URL

Example scrape config:

- job_name: blackbox
  metrics_path: /probe
  params:
    module: [http_2xx]
  static_configs:
    - targets:
        - https://argocd-server.argocd.svc
        - https://vault.vault.svc
        - http://student-api.student-api.svc/health
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - target_label: instance
      source_labels: [__param_target]
    - target_label: __address__
      replacement: blackbox-exporter.observability.svc:9115

📈 5. Enable Kubernetes & Node-Level Metrics

Prometheus must scrape:

✔ kube-state-metrics

Provides cluster object metrics (pods, deployments, PVCs, PVs).

✔ node-exporter

Provides CPU, RAM, Disk, and file system metrics.

Both should run on all nodes.

These must be installed via Helm charts.

📄 6. Configure Grafana (Dashboards + Data Sources)

Grafana must:

Run in observability namespace

Use dependent_services nodeSelector

Include two data sources:

Prometheus datasource
http://prometheus-server.observability.svc:9090

Loki datasource
http://loki.observability.svc:3100


You should also import dashboards for:

API latency

Node exporter / machine metrics

DB metrics

ArgoCD latency

Vault health

Pod health

Log insights

📁 7. Directory Structure (Helm Charts & Configs)

Ensure all charts and configs are committed in your GitHub repository:

helm/
  observability/
    prometheus/
    loki/
    grafana/
    promtail/
    blackbox-exporter/
    db-exporter/
    kube-state-metrics/
    node-exporter/

observability-configs/
  dashboards/
  loki-values.yaml
  prom-values.yaml
  promtail-values.yaml

📘 Deployment Instructions (README)
1. Create namespace
kubectl create namespace observability

2. Label the dependent_services node
kubectl label node <NODE_NAME> type=dependent_services

3. Deploy Prometheus + exporters
helm install prometheus ./helm/observability/prometheus -n observability

4. Deploy Loki
helm install loki ./helm/observability/loki -n observability

5. Deploy Promtail
helm install promtail ./helm/observability/promtail -n observability

6. Deploy Grafana
helm install grafana ./helm/observability/grafana -n observability

7. Deploy DB exporter
helm install db-exporter ./helm/observability/db-exporter -n observability

8. Deploy Blackbox exporter
helm install blackbox ./helm/observability/blackbox-exporter -n observability

---------------------------------------------

11 – Configure Dashboards & Alerts
🎯 Learning Outcomes

By completing this milestone, you will gain hands-on knowledge of:

Key Observability Pillars (Logs, Metrics, Traces)

USE (Utilization, Saturation, Errors) and RED (Rate, Errors, Duration) metrics

Grafana dashboards creation & management

Alerting best practices (Prometheus + Alertmanager + Slack notifications)

📌 Problem Statement

To make our system fully observable and production-ready, we must configure:

Grafana dashboards for each major component

Prometheus alerting rules for critical failure scenarios

Slack integration to notify alerts in real time

These dashboards and alerts will give clear visibility into:

Application performance

Database health

System resource utilization

Kubernetes object states

External endpoint uptime via Blackbox exporter

Error spikes + latency issues

All dashboards and alerts must be created declaratively and stored inside the GitHub repository.

✅ Expectations

To successfully complete this milestone, ensure all of the following requirements are met.

✔️ Grafana Dashboards

You must configure and store dashboards for the following categories.
Dashboards should be imported as JSON files inside:

helm/observability-stack/grafana/dashboards/

Required dashboards:
1. DB Metrics Dashboard

DB CPU/Mem usage

Query throughput

Slow queries

Connection count

Exported metrics via DB exporter

2. Application Error Logs Dashboard

Uses Loki as the datasource:

Error count grouped by service

Correlation by pod/container

Filters for severity levels

Time-based error trends

3. Node Metrics Dashboard

Uses node-exporter + Prometheus:

CPU load

Memory utilization

Disk I/O

Network traffic

4. Kube-State Metrics Dashboard

Using kube-state-metrics data:

Pod restarts

Deployment state

CrashLoopBackOff

Replica counts

5. Blackbox Exporter Dashboard

For external & internal endpoints:

Uptime

Response status codes

Latency (p50/p90/p95/p99)

Probe success/failures

✔️ Alerting Requirements
Alerts must be defined as PrometheusRule CRDs stored at:
helm/observability-stack/prometheus/alerts/

Required alert types:
1. Disk & CPU Utilization

node_cpu_usage > X%

node_disk_usage > Y%

2. Spike in Application Error Rate

Example:

increase({job="api"} |= "ERROR" [10m]) > threshold

3. Latency Threshold Alerts

Monitor p90, p95, p99:

histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

4. High Request Rate

Detect traffic spikes:

increase(http_requests_total[5m]) > threshold

5. Pod Restart Alerts

Specifically for:

DB

HashiCorp Vault

ArgoCD Server

Example:

increase(kube_pod_container_status_restarts_total[10m]) > 0

✔️ Slack Notification Integration

You must configure Alertmanager to send alerts to Slack.

Steps:

Create a Slack Incoming Webhook URL

Add a Kubernetes Secret:

kubectl create secret generic alertmanager-slack-config \
  --from-literal=slack_api_url=<YOUR_WEBHOOK>


Reference this secret in alertmanager.yaml

Configure receivers and routes for:

Critical alerts

Warning alerts

Info alerts

Stored at:

helm/observability-stack/alertmanager/config/


Alerts should post descriptive messages including:

Alert name

Affected component

Namespace

Node

Current value

Suggested resolution

📁 Directory Structure (Required)
helm/
  observability-stack/
    grafana/
      dashboards/
        db-metrics.json
        app-logs.json
        node-metrics.json
        kube-state.json
        blackbox.json
    prometheus/
      alerts/
        cpu-disk-alerts.yaml
        latency-alerts.yaml
        error-rate-alerts.yaml
        request-rate-alerts.yaml
        pod-restart-alerts.yaml
    alertmanager/
      config/
        alertmanager.yaml

🚀 Deployment Instructions (Add to README.md)
1. Deploy Observability Helm Chart
cd helm/observability-stack
helm upgrade --install observability . -n observability

2. Verify Components
kubectl get pods -n observability
kubectl get prometheusrules -n observability
kubectl get grafanadashboards -n observability

3. Access Grafana
kubectl port-forward svc/grafana 3000:80 -n observability


Open: http://localhost:3000







