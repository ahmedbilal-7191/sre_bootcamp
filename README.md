## SRE Bootcamp – From Local to Production (Student CRUD REST API)
Built as part of an intensive SRE Bootcamp, this repository demonstrates a complete production engineering workflow, where a microservice is developed, containerized, deployed, and fully observed using industry-standard SRE and DevOps practices.The project progresses through multiple stages of the production lifecycle using:

- Containers
- CI/CD pipelines
- Bare-metal deployments
- Kubernetes
- Helm Charts
- GitOps with ArgoCD
- Observability stack (Prometheus, Loki, Grafana, Alertmanager)
- Dashboards & Alerts

Tech Stack(Application)

| Component   | Technology           |
| ----------- | -------------------- |
| Language    | Python 3             |
| Framework   | Flask                |
| ORM         | SQLAlchemy           |
| DB          | PostgreSQL           |
| Migrations  | Flask-Migrate        |
| Validation  | Marshmallow          |
| Logging     | python-json-logger   |
| Metrics     | prometheus-client    |
| WSGI Server | gunicorn             |
| Testing     | pytest, pytest-flask |
| Linting     | pylint, flake8       |

DevOps & SRE Tooling

- Docker & Docker Compose
- GitHub Actions CI/CD
- Kubernetes
- Helm Charts
- ArgoCD (GitOps)
- Prometheus
- Grafana
- Loki + Promtail
- Alertmanager
- External Secrets Operator
- Hashicorp Vault

------------------------------------------------------------------------------------------------------------------ 

## Milesstone - 1 Create a simple REST API Webserver

This milestone covers setting up the Student CRUD REST API locally using Python, virtual environments, PostgreSQL, migrations, and Makefile automation.

## Quick Start:

Prerequisites
Ensure the following are installed on your system:
Python 3.x (to run the API)
pip (Python package manager)
PostgreSQL (for the database)


Local Setup Instructions:

1.Clone the repository
```
git clone https://github.com/<your-username>/sre-bootcamp-students-api.git
cd sre-bootcamp-students-api
```

2.Create local .env by copying:
```
cp .env.example .env
```
Update values as needed for your system.

3.Create & Activate a Virtual Environment
Linux / Mac
```
python3 -m venv venv
source venv/bin/activate
```
Windows
```
python -m venv venv
venv\Scripts\activate
```

4.Install Dependencies (via Makefile)
Instead of installing manually, use:
```
make build-local-api
```
This executes:
- `python -m pip install --upgrade pip`
- `pip install --no-cache-dir -r requirements.dev.txt`

5.Run migrations
```
make migrate
```
Which internally runs:
```
flask db init
flask db migrate
flask db upgrade
```

6.Start the API
Option A — Flask Dev Server
```
make run
```
Runs:
```
python run.py
```
Option B — Gunicorn (production style)
```
make run-gunicorn
```
Runs:
```
gunicorn --bind 0.0.0.0:8000 "app:create_app()"
```

## Makefile Commands
| Command                | Description                    |
| ---------------------- | ------------------------------ |
| `make run`             | Start Flask API                |
| `make run-gunicorn`    | Start API using Gunicorn       |
| `make test`            | Run test suite                 |
| `make migrate`         | Generate migrations            |
| `make upgrade`         | Apply database migrations      |
| `make lint`            | Run flake8 & pylint            |
| `make build-local-api` | Install local dev dependencies |


## Project Structure
```
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
```
This structure supports clean scalability as the project progresses toward Docker, CI/CD, Kubernetes, Helm, ArgoCD, and Observability in later milestones.

## Architecture Overview
layered design:


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


## Database Table: `students`

The REST API stores student records in a SQL database using SQLAlchemy ORM.

The table is created using the following model:

Students Table Schema
| Column       | Type        | Constraints                         | Description                        |
| ------------ | ----------- | ----------------------------------- | ---------------------------------- |
| `id`         | Integer     | Primary Key, Auto-increment         | Unique identifier for each student |
| `name`       | String(100) | Required, Cannot contain digits     | Student’s full name                |
| `age`        | Integer     | Required, Range(5–100)              | Student’s age                      |
| `grade`      | String(20)  | Required                            | Class or grade of the student      |
| `email`      | String(120) | Required, Unique, Valid email       | Student’s email address            |
| `created_at` | DateTime    | Default = timestamp at row creation | When the record was created        |
| `updated_at` | DateTime    | Auto-updated on modification        | When the record was last updated   |

## Supported API Endpoints (v1)

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| POST   | `/api/v1/students`      | Create a new student    |
| GET    | `/api/v1/students`      | Get all students        |
| GET    | `/api/v1/students/<id>` | Get a student by ID     |
| PUT    | `/api/v1/students/<id>` | Update a student record |
| DELETE | `/api/v1/students/<id>` | Delete a student record |
| GET    | `/healthcheck`          | Health check endpoint   |


## Postman Collection

Import postman_collection.json to test the API.


Example Request:

Example Response:


## Environment Configuration

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

## Testing
```
make test
```
Runs:
`pytest --cov=app`

## Logging

```
{
  "timestamp": "2025-01-10T12:45:20Z",
  "level": "INFO",
  "logger":svcname,
  "message": "Student created",
  "log_type": "application"
}
```
------------------------------------------------------------------------

## Milestone 2 – Containerise REST API
This milestone focuses on Dockerizing the REST API following industry-standard best practices. The implementation includes building a multi-stage Dockerfile, injecting environment variables at runtime, optimizing the image size for production, tagging images using Semantic Versioning (SemVer), and running the API entirely inside Docker.

Prerequisites

Before proceeding, ensure the following tools are installed:

### Docker Engine

Install Docker using the official production-grade steps for Ubuntu:

```
# Add Docker GPG key and repository (Ubuntu)
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
Add the Docker repository:
```
echo \
"Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc" |
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null
```
Install Docker:
```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify installation:
```
docker --version
docker compose version
```

## Add User to Docker Group
Allows running Docker without sudo:
```
sudo usermod -aG docker $USER
newgrp docker
```

## Docker Usage Instructions
### Build Docker Image
Without Makefile:
```
docker build -t my-api:1.0.0 .
```
With Makefile:
```
make docker-build VERSION=1.0.0
```
## Run the API Container
Without Makefile:
```
docker run -p 5000:5000 \
  -e DB_HOST=localhost \
  -e DB_USER=root \
  -e DB_PASS=password \
  my-api:1.0.0
```

With Makefile:
```
make docker-run VERSION=1.0.0
```
### Makefile Targets Added
```
docker-build:
    docker build -t my-api:$(VERSION) .

docker-run:
    docker run -p 8080:8080 --env-file .env my-api:$(VERSION)

docker-push:
    docker push my-api:$(VERSION)
```

---------------------------------------------------------
## Milestone 3 – One-Click Local Development Setup
This milestone focuses on simplifying local development, enabling any team member to start the entire stack—even without pre-installed tools—using Docker Compose, Makefile automation, and helper scripts. The complete stack (API + Database + Migrations) can now be started with a single command, ensuring the correct startup order without manual steps.

### Makefile Targets

The Makefile now includes targets to automate:
| Target                        | Description                                 |
| ----------------------------- | ------------------------------------------- |
| `make db-start`               | Starts the database service                 |
| `make db-migrate`             | Runs database DML migrations                |
| `make docker-build`           | Builds the REST API Docker image            |
| `make api-start`              | Starts the API along with DB and migrations |
| `make setup-tools` (optional) | Installs required tools using bash scripts  |

### Step-by-Step Local Setup

1.Start the Database
```
make db-start
```
- Starts the DB container
- Creates the network if needed

2️.Run Database DML Migrations
```
make db-migrate
```

- Check whether DB is reachable
- Applies all DML migrations
Alternatively, you can run migrations directly using the backend container:
```
docker compose run --rm backend flask db migrate
docker compose run --rm backend flask db upgrade
```

3️.Build the API Docker Image
```
make docker-build VERSION=1.0.0
```
- Uses Semantic Versioning (SemVer)

4️.Start the REST API
```
make api-start VERSION=1.0.0
```
- Starts the DB if not already running
- Applies migrations
- Builds the API Docker image if missing
- Starts the API container via Docker Compose
This ensures the stack is fully functional with a single command.

## Docker Compose Overview
The docker-compose.yml defines:

- database service
- api service
- Shared network
- Environment variables
- Service dependencies (depends_on)

This guarantees that the API waits until the database is ready.

## Makefile Overview

Example Makefile targets:
```
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
```
Ensure to change makefile values acccordingly 
	
-------------------------------------------

## Milestone 4 – Continuous Integration (CI) Pipeline Setup

This milestone introduces a fully automated CI pipeline using GitHub Actions, executed on a self-hosted runner. The goal is to ensure code quality, automated builds, testing, linting, and Docker image publishing, triggered only when relevant changes occur.

### CI Workflow Stages

The CI pipeline executes the following stages in order:

Build API
Uses a Makefile target (e.g., make build) to guarantee consistent builds across local and CI environments.

Run Tests
Executes unit and integration tests using make test to ensure code correctness before creating Docker images.

Perform Code Linting
Runs make lint (using flake8 and pylint) to enforce code quality and styling standards.

Docker Login
Authenticates to Docker Hub using GitHub Secrets (DOCKER_USERNAME and DOCKER_PASSWORD) to enable image publishing.

Docker Build & Push
Builds and pushes Docker images using either Makefile targets or GitHub’s official Docker actions. Images follow Semantic Versioning (SemVer).

### Makefile Integration

All core actions—build, test, and lint—are executed via Makefile targets to avoid duplicating logic in CI scripts.

### Self-Hosted GitHub Runner

The pipeline runs on a self-hosted runner installed locally. Key features:
- Manual Trigger Enabled:
Can be run on-demand via GitHub Actions UI using:
workflow_dispatch:

- Local Runner Setup:
GitHub Docs – Add self-hosted runners: https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners
------------------------------------------------

## Milestone 5 — Deploy REST API & Dependent Services on Bare Metal
This milestone focuses on deploying the REST API and supporting services on a bare-metal VM using Vagrant, Bash provisioning, Docker Compose, and Nginx load balancing.

### Deployment Overview
The deployment stack includes:
- Vagrant – provisions the bare-metal VM
- Bash Script – automates OS setup, installs Docker, Docker Compose, Git, Python, and adds users to the Docker group
- Docker Compose – orchestrates containers (API, DB, Nginx)
- Makefile – simplifies deployment commands
- Nginx – load balances traffic across multiple API replicas

### Infrastructure Provisioning

#### Vagrant Setup:
- Spins up a VM with CPU, memory, and networking configs
- Sets up synced folders (optional)
- Calls provisioning script (bootstrap.sh or similar)

#### Bash Script Provisioning:
- Modular functions for idempotent setup
- Installs Docker, Docker Compose, Git, curl/wget, Python
- Adds users to the Docker group
- Performs system updates and service setup

#### Application Deployment

The deployment runs 4 containers:
| Service | Purpose                               |
| ------- | ------------------------------------- |
| API-1   | REST API instance                     |
| API-2   | REST API instance                     |
| DB      | Database container (PostgreSQL/MySQL) |
| Nginx   | Load balancer for API replicas        |

#### Docker Compose features:

- Shared network
- Environment variable injection
- depends_on to ensure API starts after DB

#### Makefile Targets:

- setup → pulls Docker images
- up → runs containers in detached mode
- down → stops containers
- logs → streams container logs

#### Nginx Load Balancing:

- Configured using nginx/nginx.conf

- Performs round-robin load balancing across API replicas

- Users access API via host/VM port 8080

Example upstream configuration:
```
upstream api_backend {
    server api-1:5000;
    server api-2:5000;
}
```
#### Functional Validation
After deployment:

- API must be accessible at:
```
http://<vm-ip>:8080
```
- Nginx distributes traffic across both API containers
- All API endpoints return HTTP 200 OK when tested with Postman

#### Validation confirms:
- API is running
- Load balancing works correctly
- Containers are healthy
- Database connectivity is functional

#### Repository Requirements

All files required for bare-metal deployment must be included in the repository:

- Vagrantfile – VM configuration
- Provisioning bash script (provision.sh)
- docker-compose.baremetal.yml – multi-container orchestration
- Makefile – deployment automation
- nginx/nginx.conf – Nginx load balancing configuration

-------------------
## Milestone 6 — Setup Kubernetes Cluster

Prerequisites:
install the minikube from https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download 
install the kubectl from https://kubernetes.io/docs/tasks/tools/

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

volumeBindingMode: WaitForFirstConsumer

This ensures:

Kubernetes does NOT create the PV immediately

It waits until the Pod is scheduled

Then it provisions the PV on the same node (or topology zone) where the Pod is placed

Prevents scheduling failures such as:
Pod stuck in Pending due to PV in a different zone/node.

------------------------------------

Milestone 7 – Deploy REST API & Dependent Services in Kubernetes
✅ Objective

In this milestone, we migrate from bare-metal Vagrant deployments to Kubernetes-based deployments.
Your REST API, database, and supporting components are now deployed on the 3-node Minikube cluster created in the previous milestone.

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
create 3 namespace student-api ,external-secrets,vault then 
3. Deploy Vault
kubectl apply -f k8s-manifests/vault/

if want the vault to have the https certs 
# 1️⃣ Create the CA private key
openssl genrsa -out ca.key 4096

# 2️⃣ Create the CA certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -out ca.crt -subj "/C=xxx/ST=xxxxx/L=xxxxx/O=VaultCA/CN=Vault Root CA"
Now generate the Vault key and CSR (Certificate Signing Request):

openssl genrsa -out tls.key 2048
openssl req -new -key tls.key -out vault.csr -config vault-cert.cnf


Sign it with your CA:

openssl x509 -req -in vault.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out tls.crt -days 3650 -sha256 -extfile vault-cert.cnf -extensions req_ext

certs$ ls
ca.crt  ca.key  ca.srl  tls.crt  tls.key  vault-cert.cnf  vault.csr

kubectl -n vault create secret generic vault-tls \
  --from-file=tls.crt=tls.crt \
  --from-file=tls.key=tls.key \
  --from-file=ca.crt=ca.crt

  once the cert secrets is created then do

  Deploy Vault
kubectl apply -f k8s-manifests/vault/


exec into vault-0 vault then run
vault operator init
or if want to use only 1 key 

vault operator init -key-shares=1 -key-threshold=1

get those keys and unseal it 
after this directly run unseal for the vault-1,vault-2 also they will join auto since retryjoin
then exec into vault-0 pod we get vault operator raft list-peers we get all 3 followers and leaders

then enable k8s auth :

# Enable Kubernetes authentication
vault auth enable kubernetes



# Configure Kubernetes auth with proper paths
vault write auth/kubernetes/config \
  kubernetes_host="https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT" \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  issuer="https://kubernetes.default.svc.cluster.local"


then create a secretengine  path using secret only path of kv v2 using this cmd:

vault secrets enable -path=secret kv-v2

then create a policy for the role to be used by the eso think of it like a ACL's:

vault policy write eso-policy - << EOF
path "secret/data/*" {
  capabilities = ["read"]
}

path "secret/metadata/*" {
  capabilities = ["list"]
}
EOF

verify:
vault policy list


then attach this policy to this role we are creating
vault write auth/kubernetes/role/external-secrets-operator \
  bound_service_account_names=vault-auth \
  bound_service_account_namespaces=external-secrets \
  policies=eso-policy \
  ttl=1h


vault kv put secret/database POSTGRES_USER="db_user" POSTGRES_PASSWORD="db_password" POSTGRES_DB="name_db"

5. Deploy ESO + SecretStore
kubectl apply -f k8s-manifests/eso/

helm template external-secrets \
  external-secrets/external-secrets \
  -n external-secrets \
  --set installCRDs=true \
  --set nodeSelector.type=dependencies \
  --set webhook.nodeSelector.type=dependencies \
  --set certController.nodeSelector.type=dependencies \
  > k8s-manifests/eso/external-secrets.yaml

deploy it using helm only for manifests make a copy into a file then apply if from file in the external-secrets namespace 

kubectl create ns external-secrets


mount a secret for ca crt eso :

kubectl create secret generic vault-ca \
  --from-file=ca.crt=ca.crt \
  -n external-secrets

then apply eso/store-secret.yaml - it has secret store and the external secrets yaml whihch will sync secrets and apply in the student-api namespace

also if not want to use the https then dont include the volume mount in the vault config and the in the cluster store use http not https for url and dont mount the ca cert for the clustrer store too 
7. Deploy Database (Node B- already having node selector to be oon database node)
kubectl apply -f k8s-manifests/db.yaml

8. Deploy Application (Node A)
kubectl apply -f k8s-manifests/application.yaml

9. Verify Services
kubectl get pods -A
kubectl get svc -A

10. Test API
http://<minikube-ip>:32000/health

Here is the second Options:
This milestone focuses on deploying the REST API and its dependent services (database, migrations, secrets, configs) on Kubernetes.
All Kubernetes manifests, namespaces, ConfigMaps, ESO (External Secrets Operator), and Vault-based secrets must be created and deployed using standard YAML manifests.

📁 Repository Structure

All Kubernetes manifests must be committed inside the same repository:

k8s/
 ├── application/
 │    └── application.yml
 ├── database/
 │    └── database.yml
 ├── eso/
 │    ├── external-secret.yml
 │    ├── secret-store.yml
 │    └── vault-config.yml
 ├── vault/
 │    ├── deployment.yml
 │    ├── service.yml
 │    └── policies.hcl
 ├── namespaces/
 │    └── student-api-namespace.yml
 └── README.md


Each component has a single manifest file containing all required resources.

🏷 Namespaces

All application and database resources must be deployed inside:

student-api

You can create it using:

🐳 Application Component (application.yml)

The application manifest includes:

Namespace
ConfigMap
Deployment havooing init container to run the db migrations
Service

Environment variables should be provided using:

✔ ConfigMaps — non-sensitive values such as API config, ports, debug flags
✔ External Secrets (ESO) — sensitive values like DB credentials, token, password

🛢 Database Component (database.yml)

The database manifest contains:

Namespace

PVC
StorageClass reference
StatefulSet 
Service

DB migrations must run before the API container starts.

Your app deployment must include:

initContainers:
  - name: db-migrations
    image: my-api-migration-image:1.0.0
    command: ["sh", "-c", "python migrate.py"]
    envFrom:
      - secretRef:
          name: db-creds


This ensures migrations run once before the main application starts.


Wait for pods:

kubectl get pods -n student-api

🧪 Testing the API (Postman)

Once all pods are running and the service is exposed, test the API:

curl -i http://<YOUR-IP>:<PORT>/health


Expected response:

HTTP/1.1 200 OK


After this, use the Postman collection included in the repository to test:

Create Student

Get Student

Update Student

Delete Student

All endpoints must return 200 OK.


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

✔ ESO + Vault integration parameterized-can be done 

ExternalSecret template uses values like:
vault:
  path: "student-api/"
  secretKeys:
    username: db-user
    password: db-pass

✔ DB migrations handled via initContainers

Your API Helm chart includes:

initContainers:
  - name: run-migrations
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    command: ["sh", "-c", "python manage.py run_migrations"]

🚀 Deployment Workflow Using Helm
1. here in out case we have already helm manifest files for the managed chart locally present to first deploy the vault if we want the ca certs etc the process is same a sabove for the k8s manifest deployment craeating a secrets then applying as a ca to (aslo if dont want the https change config to not to use the not to mount from the secrets )the helm charts then depploy the vault using helm in the helm charts/infrastructure/vault but its override values.yaml is in overridee-values/vault-fin-1 here serverTelemetry:
  prometheusRules:
    enabled: true is true disable it if you dont have the logging and monitoring setup and its relaveant crds
then do the same steps like adding the unsealing etc same as did for the k8s-manifests then deploy the eso if using the  https deploy the secret sfor the cas ame as aboce k8s-manifest then deploy the eso in the infrastructure/external-serets file usinf a override file in the override-values/eso-fin-1.yaml

one vault is configured then deploy the eso from the helm-charts/infrastructure/external-secrets it uses ht eoverride file from the overrifde-values/eso-fin-1.yaml same before installing if you need the https of vault use the cert first make the seret sa s we did in previous milestonne ,also then apply the clusterstore present in the external-secrets/clusterstore.yaml

now simply deploy the helm chart of the backedn app present in the helm-charts/backend in the student-api namespace then its template folder has external secrets alos disable this if the log and monitoring i snot disabled 

serviceMonitor:
  enabled: true
  interval: 30s
  path: /metrics

alerts:
  enabled: true
  



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


3. Schedule ArgoCD on the dependent_services Node

in previous helm chart deployment only the argocd is present locally in the helm-charts/infrastructure/argocd and its override file is present in the override-values/values-argocd.yaml  also disable the 
controller:
  metrics:
    rules:
      enabled: true if the log and monitoring stack i s not configured 
then in the argomanifest there is external secrets.yaml which createss ync secrets for the private repo of the deployment then after that apply the app.yaml which is the application type of argocd 



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
note: also make sure you enable (by default enable the alerts and monitroing form the argocd,vault,backedn app if disabled duing the deployment using helm previoius milestone once after settting up the log an dmonitoring setup )
the helm charts for the observability stack is present locally with the override values.yaml 
also in the logging and monitoring stack we have the secrets for grafana ,alertmanager the db exporter we can also use the existing secret for this to work of the backedn secret then also the externla serets are there in their own respective folders like postgrasdb exporter template fodler has its own  externalresourece sam egoes for kube prom (alermanager) and the grafan has secerets in its on helm chart also lalerts are with them too the backedn api app has it sown alert and svc monitoring in ts template folder from valuesyaml we can envble it also the kube prmetheus stack has their own too 


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









