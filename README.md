# SRE Bootcamp – From Local to Production (Student CRUD REST API)

Built as part of an intensive SRE Bootcamp, this repository demonstrates a complete production engineering workflow, where a microservice is developed, containerized, deployed, and fully observed using industry-standard SRE and DevOps practices.The project progresses through multiple stages of the production lifecycle using:

- Containers
- CI/CD pipelines
- Bare-metal deployments
- Kubernetes
- Helm Charts
- GitOps with ArgoCD
- Observability stack (Prometheus, Loki, Grafana, Alertmanager)
- Dashboards & Alerts

## Tech Stack(Application)

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

## DevOps & SRE Tooling

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

### Prerequisites:

Ensure the following are installed on your system:
- Python 3.x (to run the API)
- pip (Python package manager)
- PostgreSQL (for the database)

### Local Setup Instructions:

#### 1.Clone the repository
```
git clone https://github.com/ahmedbilal-7191/sre_bootcamp.git
cd sre_bootcamp
```

#### 2.Create local .env by copying:
```
cp .env.example .env
```
Update values as needed for your system.

#### 3.Create & Activate a Virtual Environment

##### Linux / Mac
```
python3 -m venv venv
source venv/bin/activate
```

##### Windows
```
python -m venv venv
venv\Scripts\activate
```

#### 4.Install Dependencies (via Makefile)
Instead of installing manually, use:
```
make build
```

##### This executes:
- `python -m pip install --upgrade pip`
- `pip install --no-cache-dir -r requirements.dev.txt`

the current project has migrations folder to github so if wantt o use thaat  no need to initializa if begeing withou the migrations folder then 

#### 5.Initialize DB Migrations (run once)
```
make migrate-init
```

#### 6.Create a Migration(Generate migration scripts)
```
make migrate-create M="create students table"
```
Which internally runs:
```
flask db migrate -m "$(M)"
```

#### 7.Apply Migrations
```
make migrate-upgrade
```
Which internally runs:
```
flask db upgrade
```

#### 8.Start the API

##### Option A — Flask Dev Server
```
make run
```
##### Runs:
```
python run.py
```

##### Option B — Gunicorn (production style)
```
make run-gunicorn
```
##### Runs:
```
gunicorn --bind 0.0.0.0:8000 "app:create_app()"
```

### Health Check
```
curl http://localhost:5000/healthcheck
```

### Makefile Commands

| Command                               | Description                    |
| ------------------------------------- | ------------------------------ |
| `make run`                            | Start Flask API                |
| `make run-gunicorn`                   | Start API using Gunicorn       |
| `make test`                           | Run test suite                 |
| `make migrate-create M="message"`     | Generate a new migration script|
| `make migrate-upgrade`                | Apply database migrations      |
| `make lint`                           | Run flake8 & pylint            |
| `make migrate-init`                   | Initialize Alembic migrations (run once) |
| `make build`                          | Install local dev dependencies |


### Project Structure

```
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

### Architecture Overview

#### layered design:

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
         │            PostgreSQL                  │
         │         (via SQLAlchemy ORM)           │
         └────────────────────────────────────────┘


### Database Table: `students`

The REST API stores student records in a SQL database using SQLAlchemy ORM.

The table is created using the following model:

### `Students` Table Schema

| Column       | Type        | Constraints                         | Description                        |
| ------------ | ----------- | ----------------------------------- | ---------------------------------- |
| `id`         | Integer     | Primary Key, Auto-increment         | Unique identifier for each student |
| `name`       | String(100) | Required, Cannot contain digits     | Student’s full name                |
| `age`        | Integer     | Required, Range(5–100)              | Student’s age                      |
| `grade`      | String(20)  | Required                            | Class or grade of the student      |
| `email`      | String(120) | Required, Unique, Valid email       | Student’s email address            |
| `created_at` | DateTime    | Default = timestamp at row creation | When the record was created        |
| `updated_at` | DateTime    | Auto-updated on modification        | When the record was last updated   |

### Supported API Endpoints (v1)

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| POST   | `/api/v1/students`      | Create a new student    |
| GET    | `/api/v1/students`      | Get all students        |
| GET    | `/api/v1/students/<id>` | Get a student by ID     |
| PUT    | `/api/v1/students/<id>` | Update a student record |
| DELETE | `/api/v1/students/<id>` | Delete a student record |
| GET    | `/healthcheck`          | Health check endpoint   |


### Postman Collection

Import postman_collection.json to test the API.


Example Request:

Example Response:


### Environment Configuration

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

### Testing
```
make test
```
Runs:
`pytest -v --cov=app --cov-report=term-missing`

### Logging
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

### Prerequisites

Before proceeding, ensure the following tools are installed:

#### Docker Engine

##### 1.Install Docker using the official production-grade steps for Ubuntu:
```
# Add Docker GPG key and repository (Ubuntu)
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

##### 2.Add the Docker repository:
```
echo \
"Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc" |
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null
```

##### 3.Install Docker:
```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

##### 4.Verify installation:
```
docker --version
docker compose version
```

##### 5.Add User to Docker Group

##### Allows running Docker without sudo:
```
sudo usermod -aG docker $USER
newgrp docker
```

### Docker Usage Instructions

#### 1.Build Docker Image

Without Makefile:
```
docker build -t my-api:1.0.0 .
```
With Makefile:
```
make docker-build
```

#### 2.Run the API Container

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
make docker-run
```

---------------------------------------------------------
## Milestone 3 – One-Click Local Development Setup
This milestone focuses on simplifying local development, enabling any team member to start the entire stack—even without pre-installed tools—using Docker Compose, Makefile automation, and helper scripts. The complete stack (API + Database + Migrations) can now be started with a single command, ensuring the correct startup order without manual steps.

### Makefile Targets

#### The Makefile now includes targets to automate:

| Target                        | Description                                 |
| ----------------------------- | ------------------------------------------- |
| `make db-up`                  | Starts the database service                 |
| `make db-down`                | Runs database DML migrations                |
| `make db-status`              | Show database container status            |
| `make docker-build`              | Build the REST API Docker image (SemVer tagging supported) | 
| `make docker-run` | Run the API container using `.env`  |
| `make compose-build`  | Build all Docker Compose services  |
| `make compose-up`  | Start DB → run migrations → start API  |
| `make compose-down`  | Stop all Docker Compose services  |

### Step-by-Step Local Setup

#### 1.Start the Database
```
make db-up
```
- Starts the DB container
- Creates the network if needed

#### 2️.Run Database DML Migrations to be done
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

#### 3️.Build the API Docker Image
```
make compose-build
```
- Uses Semantic Versioning (SemVer)

#### 4.Start the REST API-Start DB, run migrations, and start API:
```
make compose-up
```
- Starts the DB if not already running
- Applies migrations
- Builds the API Docker image if missing
- Starts the API container via Docker Compose
This ensures the stack is fully functional with a single command.

#### 5.Stop services
```
make compose-down
```

### Docker Compose Overview

#### The docker-compose.yml defines:
- database service
- api service
- Shared network
- Environment variables
- Service dependencies (depends_on)

This guarantees that the API waits until the database is ready.	

-------------------------------------------

## Milestone 4 – Continuous Integration (CI) Pipeline Setup

This milestone introduces a fully automated CI pipeline using GitHub Actions, executed on a self-hosted runner. The goal is to ensure code quality, automated builds, testing, linting, and Docker image publishing, triggered only when relevant changes occur.

### CI Workflow Stages

#### The CI pipeline executes the following stages in order:

- `Build API`
Uses a Makefile target (e.g., make build) to guarantee consistent builds across local and CI environments.

- `Run Tests`
Executes unit tests using make test to ensure code correctness before creating Docker images.

- `Perform Code Linting`
Runs make lint (using flake8 and pylint) to enforce code quality and styling standards.

- `Docker Login`
Authenticates to Docker Hub using GitHub Secrets (DOCKER_USERNAME and DOCKER_PASSWORD) to enable image publishing.

- `Docker Build & Push`
Builds and pushes Docker images using either Makefile targets or GitHub’s official Docker actions. Images follow Semantic Versioning (SemVer).

### Makefile Integration

All core actions—build, test, and lint—are executed via Makefile targets to avoid duplicating logic in CI scripts.

### Self-Hosted GitHub Runner

#### The pipeline runs on a self-hosted runner installed locally.

#### Key features:
- Manual Trigger Enabled:
Can be run on-demand via GitHub Actions UI using:
workflow_dispatch:

- Local Runner Setup:
GitHub Docs – Add self-hosted runners: https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners
------------------------------------------------

## Milestone 5 — Deploy REST API & Dependent Services on Bare Metal
This milestone focuses on deploying the REST API and supporting services on a bare-metal VM using Vagrant, Bash provisioning, Docker Compose, and Nginx load balancing.

![milestone5-j](https://github.com/user-attachments/assets/69cd861a-a193-47de-bee9-37b6bf89c6ba)

### Repository Requirements

```
├── Vagrantfile
├── Dockerfile
├── provision.sh
├── Makefile
├── docker-compose.yml
├── docker-compose.baremetal.yml
├── nginx/
│   └── nginx.conf
├── app/
├── migrations/
└── README.md
```

### Prerequisites (Host)

- Vagrant
- VirtualBox

### Step-by-Step Local Setup

#### 1.Start the VM
```
vagrant up
vagrant ssh
```
What This Does

- Provisions Ubuntu VM
- Installs Docker, Compose, Make

#### 2.Deploy Full Stack 
```
cd /vagrant
make deploy-baremetal
```

Starts:

2 API containers

1 PostgreSQL container

1 Nginx load balancer

Runs DB migrations automatically




#### 3.Access API (via Nginx)
```
http://localhost:8080
```

#### 4.Health check:
```
curl http://localhost:8080/healthcheck
```
Status: 200 OK
Traffic load-balanced across both APIs

### Functional Validation

#### After deployment:

- API must be accessible at:
```
http://<vm-ip>:8080
```
- Nginx distributes traffic across both API containers
- All API endpoints return HTTP 200 OK when tested with Postman

### Stop and remove bare-metal deployment

```
make destroy-baremetal
```

### Nginx Load Balancing:

- Configured using nginx/nginx.conf

- Performs round-robin load balancing across API replicas

- Users access API via host/VM port 8080

#### Example upstream configuration:
```
upstream api_backend {
    server api-1:5000;
    server api-2:5000;
}
```

### Deployment Overview

#### The deployment stack includes:

- Vagrant – provisions the bare-metal VM
- Bash Script – automates OS setup, installs Docker, Docker Compose, Git, Python, and adds users to the Docker group
- Docker Compose – orchestrates containers (API, DB, Nginx)
- Makefile – simplifies deployment commands
- Nginx – load balances traffic across multiple API replicas

-------------------

## Milestone 6 — Setup Kubernetes Cluster

This milestone focuses on setting up a production-like Kubernetes cluster using Minikube with three worker nodes, each labeled to represent different workload responsibilities.
This prepares the cluster for deploying the application, database, and dependent services in later milestones.

### Prerequisites:

#### Ensure the following tools are installed on your system:

- minikube
https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download 
- kubectl
https://kubernetes.io/docs/tasks/tools/
#### Verify installation:

```
minikube version
kubectl version --client
```
### Step-by-Step Local Setup

#### 1.Create a Multi-Node Minikube Cluster
```
minikube start --nodes 4 -p prod-cluster
```
##### verify nodes:
```
kubectl get nodes
```

#### 2️.Label the Worker Nodes Appropriately

##### Add labels to instruct the scheduler where to run future workloads:

Worker Node	Label
Node A	type=application
Node B	type=database
Node C	type=dependent_services

##### Example:
```
kubectl label node prod-cluster-m02 type=application
kubectl label node prod-cluster-m03 type=database
kubectl label node prod-cluster-m04 type=dependent_services
```

##### verify lables:
```
kubectl get nodes --show-labels
```

These labels will later be used in Deployment manifests:

nodeSelector:
  type: application


#### 3️.Enable CSI HostPath Storage Driver

To support multi-node persistent storage, enable Minikube’s CSI HostPath driver:
```
minikube addons enable csi-hostpath-driver -p prod-cluster
```
This enables CSI-backed dynamic volume provisioning, which is required for stateful workloads in multi-node clusters.

#### 4️.Configure the Default StorageClass

Minikube’s default standard StorageClass is not suitable for multi-node workloads. To ensure reliable storage provisioning for stateful components, the CSI HostPath StorageClass is configured as the default for this cluster.

##### 4.1 Set CSI HostPath as Default

###### Edit the CSI StorageClass:
```
kubectl edit storageclass csi-hostpath-sc
```

###### Ensure it includes:
```
metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
```

#### 4.2 (Optional but Recommended) Remove Default Annotation from Old StorageClass

To avoid conflicts between multiple default StorageClasses, remove the default annotation from Minikube’s standard StorageClass:
```
kubectl patch storageclass standard -p \
'{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```
What This Ensures
With CSI HostPath configured as the default, all future PVCs automatically use it. PersistentVolumes are created on the same node where the Pod is scheduled, making this setup ideal for databases and other stateful components.

### Why CSI HostPath Matters

The default Minikube storage works reliably only in single-node clusters. In a multi-node setup, CSI HostPath ensures that each worker node uses its own CSI driver and that volumes are provisioned per node. This allows storage to fully respect Kubernetes pod scheduling decisions.

This design aligns naturally with node-based workload placement, ensuring that database pods, application pods, and dependent services use storage from the same nodes on which they run, preventing cross-node storage conflicts.

### volumeBindingMode: WaitForFirstConsumer

The CSI HostPath StorageClass uses volumeBindingMode: WaitForFirstConsumer. This means Kubernetes does not provision a PersistentVolume immediately. Instead, it waits until the Pod is scheduled and then creates the volume on the same node as the Pod.

This behavior prevents common issues such as Pods stuck in a Pending state, volumes being created on incorrect nodes, and node affinity or scheduling conflicts.

------------------------------------

## Milestone 7 – Deploy REST API & Dependent Services in Kubernetes

In this milestone, we migrate from bare-metal Vagrant deployments to Kubernetes-based deployments using Minikube. The Student REST API, PostgreSQL database, and dependent services such as HashiCorp Vault and External Secrets Operator (ESO) are deployed on a 3-node Minikube cluster created in the previous milestone.

![milestone7-j](https://github.com/user-attachments/assets/d2782692-730f-476d-a47a-bf61b49018d7)


### Repository Structure (Kubernetes Manifests)

#### All Kubernetes manifests are committed to the same repository under the following structure:
```
k8s-manifests/
├── application.yaml
├── database.yaml
├── eso/
│   ├── store-secret.yaml
├── vault/
│   ├── vault.yaml
```

### Namespaces

#### Create the required namespaces before deployment:
```
kubectl create namespace student-api
kubectl create namespace vault
kubectl create namespace external-secrets
```

### Optional: Enable TLS for Vault
-------------
#### Generate a CA certificate:
```
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -out ca.crt -subj "/C=xxx/ST=xxxxx/L=xxxxx/O=VaultCA/CN=Vault Root CA"
```

#### Generate Vault Cert
```
openssl genrsa -out tls.key 2048
openssl req -new -key tls.key -out vault.csr -config vault-cert.cnf
openssl x509 -req -in vault.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out tls.crt -days 3650 -sha256 -extfile vault-cert.cnf -extensions req_ext
```

#### files generated:
`
certs$ ls
ca.crt  ca.key  ca.srl  tls.crt  tls.key  vault-cert.cnf  vault.csr
`

#### Create the TLS secret:
```
kubectl -n vault create secret generic vault-tls \
  --from-file=tls.crt=tls.crt \
  --from-file=tls.key=tls.key \
  --from-file=ca.crt=ca.crt
```
--------------------------

### Deployment Steps:

#### 1.Deploy Vault (Node C – dependent_services)
```
kubectl apply -f k8s-manifests/vault/
```
Vault pods are scheduled on the dependent_services node using nodeSelector.

##### Initialize & Configure Vault:
```
kubectl exec -it vault-0 -n vault -- vault operator init -key-shares=1 -key-threshold=1
kubectl exec -it vault-0 -n vault -- vault operator unseal
```
Unseal the remaining Vault pods (vault-1, vault-2).

##### Verify raft cluster:
```
vault operator raft list-peers
```

##### Enable Kubernetes Authentication in Vault

##### Enable Kubernetes authentication
```
vault auth enable kubernetes
```

##### Configure Kubernetes authentication:
```
vault write auth/kubernetes/config \
  kubernetes_host="https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT" \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  issuer="https://kubernetes.default.svc.cluster.local"
```

##### Enable KV v2 secrets engine:
```
vault secrets enable -path=secret kv-v2
```

##### Create policy for ESO:
```
vault policy write eso-policy - << EOF
path "secret/data/*" {
  capabilities = ["read"]
}
path "secret/metadata/*" {
  capabilities = ["list"]
}
EOF
```
##### verify:
```
vault policy list
```

##### Create Vault role for ESO:
```
vault write auth/kubernetes/role/external-secrets-operator \
  bound_service_account_names=vault-auth \
  bound_service_account_namespaces=external-secrets \
  policies=eso-policy \
  ttl=1h
```

##### Store database credentials:
```
vault kv put secret/database POSTGRES_USER="db_user" POSTGRES_PASSWORD="db_password" POSTGRES_DB="name_db"
```

#### 2.Deploy External Secrets Operator (ESO)

ESO is deployed using Helm and rendered into Kubernetes manifests

helm template external-secrets \
  external-secrets/external-secrets \
  -n external-secrets \
  --set installCRDs=true \
  --set nodeSelector.type=dependent_services \
  --set webhook.nodeSelector.type=dependent_services \
  --set certController.nodeSelector.type=dependent_services 

##### Apply the generated manifest or use the rendered file:
```
kubectl apply -f k8s-manifests/eso/external-secrets.yaml
```

##### Create CA secret for ESO (if using HTTPS):
```
kubectl create secret generic vault-ca \
  --from-file=ca.crt=ca.crt \
  -n external-secrets
```

##### Apply SecretStore and ExternalSecret:
```
kubectl apply -f k8s-manifests/eso/store-secret.yaml
```
If HTTPS is not used, remove CA mounts and use HTTP in the Vault URL.

#### 3.Deploy Database (Node B)
```
kubectl apply -f k8s-manifests/database.yaml
```
The database pod is scheduled on Node B using a node selector.

#### 4.Deploy Application (Node A)
```
kubectl apply -f k8s-manifests/application.yaml
```

Database Migrations (Init Container)
Database migrations are executed using an init container before the main application starts:
```
- name: migrate-container
  image: backend-backend:v1.0.0
  envFrom:
    - configMapRef:
        name: backend-config
    - secretRef:
        name: db-secrets
  command: ["sh", "-c"]
  args: ["echo 'Running migrations...' && flask db upgrade && echo 'Migrations complete.'"]
```

This ensures migrations run once and before application startup.

### Verification

#### Verify pods and services:
```
kubectl get pods -A
kubectl get svc -A
```

### Test health endpoint:
```
curl -i http://<NODE_IP>:32000/health
```

Expected response:

HTTP/1.1 200 OK

### API Testing (Postman)

After successful deployment, use the Postman collection included in the repository to test:

Create Student

Get Student

Update Student

Delete Student

All endpoints should return 200 OK.

---------------------------
## Milestone 8 – Deploy REST API & Dependent Services Using Helm Charts

In this milestone, we transition from raw Kubernetes manifests to Helm-based deployments for the REST API, PostgreSQL database, Vault, and External Secrets Operator (ESO).
Helm enables packaging, versioning, configuration overrides, and reusable deployments, making the setup closer to production standards.

### Helm Repository Structure

```
helm-charts/
├── backend/
├── infrastructure/
│   ├── vault/
│   └── external-secrets/
└── override-values/
    ├── vault-fin-1.yaml
    └── eso-fin-1.yaml

```

### Deployment Workflow Using Helm

#### 1.Deploy Vault (Infrastructure)

Vault is deployed first since it is required by ESO.

TLS setup (CA, server certs, Kubernetes secret) is same as Milestone 7

If HTTPS is not required, disable TLS mounts and use HTTP in values

##### Deploy Vault using Helm:
```
helm install vault helm-charts/infrastructure/vault \
  -n vault \
  -f override-values/vault-fin-1.yaml
```

##### Important Notes

- serverTelemetry.prometheusRules.enabled: true
- Disable this if the observability stack (Prometheus CRDs) is not installed.

Vault pods are scheduled using node selectors (dependent services node).

##### Initialize & Unseal Vault

Same as the previous milestone:
```
vault operator init
vault operator unseal
vault operator raft list-peers
```

##### Configure Vault for Kubernetes & ESO

Inside the Vault pod:
- Enable Kubernetes auth
- Enable KV v2 secrets engine
- Create ESO read-only policy
- Bind policy to ESO Kubernetes role
- Store database credentials
(Exact commands remain unchanged from Milestone 7.)

#### 2.Deploy External Secrets Operator (ESO)

If Vault uses HTTPS:
- Create CA secret in external-secrets namespace (same as before)

##### Deploy ESO using Helm:
```
helm install external-secrets helm-charts/infrastructure/external-secrets \
  -n external-secrets \
  -f override-values/eso-fin-1.yaml
```

##### Apply ClusterSecretStore:
```
kubectl apply -f external-secrets/clusterstore.yaml
```

Once configured, ESO automatically syncs secrets from Vault into the target namespaces.

#### 3.Deploy Backend Application (Student API)

Deploy the backend Helm chart:
```
helm install student-api helm-charts/backend -n student-api
```

#### Notes

- The backend chart includes ExternalSecret templates
- Disable the following if observability is not installed:
```
serviceMonitor:
  enabled: false

alerts:
  enabled: false
```

- Database migrations run using an init container before the main app starts

### Access the REST API

If using NodePort:
```
kubectl get svc -n student-api
```

Example URL:
```
http://<NODE-IP>:32000
```

### API Testing

Test using Postman or curl:
```
GET  /students  → 200 OK
POST /students  → 200 OK
```

All CRUD endpoints must return 200 OK.

--------------------------------------------------------

## Milestone 9 — Setup One-Click Deployments Using ArgoCD

This milestone introduces GitOps-based automated deployments using ArgoCD.
Instead of manually running kubectl apply or helm install, ArgoCD continuously watches the Git repository and automatically synchronizes Kubernetes state whenever changes are pushed.
![milestone9-j](https://github.com/user-attachments/assets/c4ff0787-d450-4efe-8777-d5185e99819b)

### Repository Layout for GitOps

Your repo now includes:
```
argomanifest/
├── app.yaml
└── external-secrets.yaml

helm-charts/
├── backend/
├── infrastructure/
│   ├── vault/
│   ├── external-secrets/
│   └── argo-cd/
│
└── override-values/
    ├── vault-fin-1.yaml
    ├── eso-fin-1.yaml
    └── values-argocd.yaml
```

### ArgoCD Installation & Setup

ArgoCD is installed using a locally managed Helm chart.

#### Install ArgoCD
```
helm install argocd helm-charts/infrastructure/argo-cd \
  -n argocd \
  -f override-values/values-argocd.yaml
```

#### Scheduling & Observability Notes

- ArgoCD is scheduled on the dependent_services node
- Disable the following if the logging/monitoring stack is not installed:
```
controller:
  metrics:
    rules:
      enabled: false
```

### GitOps Secrets via External Secrets

The argomanifest/external-secrets.yaml file configures External Secrets for ArgoCD.

- Syncs credentials for private Git repositories
- Uses an existing ClusterSecretStore (already applied in previous milestones)
- Secrets are automatically injected into the ArgoCD namespace

#### Apply it once:
```
kubectl apply -f argomanifest/external-secrets.yaml
```

### One-Click Application Deployment via ArgoCD

#### Deploy applications by applying the ArgoCD Application manifest:
```
kubectl apply -f argomanifest/app.yaml
```

This enables:
- Automatic Helm chart deployment
- Continuous sync with Git
- Self-healing and drift correction

No manual Helm or kubectl commands are required after this.

### CI Workflow – Automated Image Updates

The GitHub Actions CI pipeline now includes an additional GitOps step.

What Happens After CI Success

- Build, test, lint, and push Docker image

- Pull the Helm chart from the repository

- Update the image tag in values.yaml

- Commit and push the change to main

### Result

ArgoCD automatically detects the update and deploys the new version — true one-click deployment.

### Access ArgoCD UI (Optional)

#### Port-forward ArgoCD Server
```
kubectl port-forward svc/argocd-server -n argocd 8080:80
```

### Access UI:
```
http://localhost:8080
```

### Retrieve Initial Admin Password
```
kubectl get secret argocd-initial-admin-secret \
  -n argocd \
  -o jsonpath="{.data.password}" | base64 -d
```
----------------------------------

## Milestone 10 — Setup an Observability Stack (Prometheus, Loki, Grafana, Promtail) 
This milestone focuses on setting up a complete observability stack in Kubernetes using Prometheus, Loki, and Grafana, deployed on the dependent_services node under the observability namespace.

The setup enables:

- Centralized metrics collection
- Centralized log aggregation
- Database monitoring
- Internal endpoint monitoring
- Unified visualization via Grafana

### Components Overview

#### Prometheus (kube-prometheus-stack)

##### Scrapes:
- Node metrics
- kube-state-metrics
- DB exporter metrics
- Blackbox exporter metrics

##### Includes:
- Alertmanager
- Custom infra alerts (CPU & storage)

Deployed in observability namespace

#### Loki
- Central log storage
- Uses Loki Gateway
- Integrated with Grafana for log querying

#### Promtail
- Collects only application logs
- Configured via quick2.yaml
- Sends logs exclusively to Loki Gateway

#### PostgreSQL Exporter
- Monitors DB metrics for backend API(Running in the student-api ns)
- Uses External Secrets to fetch DB credentials securely

#### Blackbox Exporter
- Monitors internal HTTP/HTTPS endpoints
- Used for service availability and health checks

#### Grafana
- Deployed with Helm
- Configured datasources(Sidecar):
  - Prometheus → Metrics
  - Loki → Logs
- Secrets for admin credentials managed via Helm templates
- Dashboards & alerts enabled

### Secrets & External Secrets
The following components manage secrets internally via Helm templates or External Secrets:
| Component             | Secret Handling                         |
| --------------------- | --------------------------------------- |
| Grafana               | External secrets                        |
| Alertmanager(API URL) | External Secrets                        |
| PostgreSQL Exporter   | External Secrets                        |
| Backend API           | ServiceMonitor & alerts via Helm values |

### Important Note (Alerts & Monitoring)

If alerts or ServiceMonitors were disabled in previous milestones (ArgoCD, Vault, Backend API),
re-enable them now after setting up the logging and monitoring stack.

This ensures:

Metrics are scraped correctly
Alerts are fired as expected
Dashboards show complete data



### Deployment Instructions
#### Step 1: Create Namespace
```
kubectl create namespace observability
```

#### Step 2: Deploy kube-prometheus-stack
```
helm install prometheus \
  ./kube-prometheus-stack \
  -f ./override-values/values-kube-prome-stack.yaml \
  -n observability
```

#### Step 3: Deploy Loki
```
helm install loki \
  ./loki \
  -f ./override-values/loki-doc.yaml \
  -n observability
```

#### Step 4: Deploy Promtail (Application Logs Only)
```
helm install promtail \
  ./promtail \
  -f ./override-values/quick2.yaml \
  -n observability
```

#### Step 5: Deploy PostgreSQL Exporter
```
helm install postgres-exporter \
  ./postgres-exporter \
  -f ./override-values/values-postgres-exporter.yaml \
  -n observability
```

#### Step 6: Deploy Blackbox Exporter
```
helm install blackbox-exporter \
  ./blackbox-exporter \
  -f ./override-values/values-blackbox-exporter.yaml \
  -n observability
```

#### Step 7: Deploy Grafana
helm install grafana \
  ./grafana \
  -f ./override-values/values-grafana.yaml \
  -n observability


### Validation Checklist

- Prometheus targets show UP
- Loki receiving application logs
- Grafana dashboards load metrics & logs
- DB exporter metrics visible
- Blackbox probes reporting status
- Alerts visible in Alertmanager

---------------------------------------------

## 11 – Configure Dashboards & Alerts

This milestone focuses on operational observability at runtime by configuring Grafana dashboards and Prometheus alerts to monitor system health, application behavior, and infrastructure reliability.
Additionally, Slack notifications are configured to ensure alerts are delivered with clear, actionable messages.

### Repository Structure
```
logging-monitoring/
├── grafana/
│   ├── templates/
│   │   └── datasources-secrets/
│   │       ├── prom-ds.yaml        # Prometheus datasource (Secret)
│   │       └── loki-ds.yaml        # Loki datasource (Secret)
│   ├── dashboards/                # Legacy reference (not mounted directly)
│   └── values.yaml
│
├── kube-prometheus-stack/
│   └── templates/
│       ├── alertmanager/
│       │   └── externalsecret.yaml
│       └── prometheus/
│           └── dashboards-cm/
│               ├── node-exporter-cm.yaml
│               └── kube-state-dash-cm.yaml
│
├── postgres-exporter/
│   └── templates/
│       └── dashboard-cm/
│           └── postgres-dash-cm.yaml
│
├── backend/
│   └── templates/
│       ├── dashboard-cm/
│       └── alerts/
│
├── blackbox-exporter/
│   └── templates/
│       └── dashboard-cm/
│
└── override-values/
    └── values-kube-prome-stack.yaml

```

### Grafana Dashboards Configuration
#### Dashboards are owned by the component they observe and exposed to Grafana via ConfigMaps rendered using .Files.Get.

#### Configured Dashboards
| Component                  | Dashboard Source                                                | ConfigMap Location                                                                 |
| -------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Node metrics               | `kube-prometheus-stack/dashboards/node-exporter-dashboard.json` | `kube-prometheus-stack/templates/prometheus/dashboards-cm/node-exporter-cm.yaml`   |
| Kubernetes state           | `kube-prometheus-stack/dashboards/kube-state.json`              | `kube-prometheus-stack/templates/prometheus/dashboards-cm/kube-state-dash-cm.yaml` |
| PostgreSQL                 | `postgres-exporter/dashboards/postgres-exporter.json`           | `postgres-exporter/templates/dashboard-cm/postgres-dash-cm.yaml`                   |
| Application metrics & logs | `backend/dashboards/*.json`                                     | `backend/templates/dashboard-cm/`                                                  |
| Blackbox probing           | `blackbox-exporter/dashboards/*.json`                           | `blackbox-exporter/templates/dashboard-cm/`                                        |

#### Alerting Strategy

#### Infrastructure Alerts (Prometheus)

Defined under:
```
kube-prometheus-stack/templates/prometheus/custom-alerts/
```
Alerts include:
- High CPU utilization
- High disk utilization

These alerts apply cluster-wide and run in the observability namespace.

#### Application Alerts
Defined inside the backend Helm chart under:
```
backend/templates/
```
Application-level alerts include:
- Error rate spike in last 10 minutes
- Increased request rate
- Latency threshold breaches:
  - p90
  - p95
  - p99
These alerts are enabled via backend Helm values.yaml.

#### Restart Alerts
Restart alerts for:
- Database
- HashiCorp Vault
- ArgoCD

are enabled via:
```
override-values/values-kube-prome-stack.yaml
```
using Alertmanager rules exposed by kube-prometheus-stack.

#### Slack Alert Notifications

All alerts are delivered to Slack with descriptive messages.

Slack Integration Details

Slack Webhook URL is NOT hardcoded

Retrieved securely using External Secrets

ExternalSecret is located at:
```
kube-prometheus-stack/templates/alertmanager/externalsecret.yaml
```

#### Alert Scenarios Covered
| Scenario                       | Alert Source            |
| ------------------------------ | ----------------------- |
| CPU & Disk threshold breach    | Prometheus infra alerts |
| Error rate spike (10 min)      | Backend alerts          |
| Latency increase (p90/p95/p99) | Backend alerts          |
| High request volume            | Backend alerts          |
| DB restart                     | kube-state-metrics      |
| Vault restart                  | kube-state-metrics      |
| ArgoCD restart                 | kube-state-metrics      |

#### Deployment Notes

#### Important
Ensure alerting and ServiceMonitor flags are enabled for:
- Backend application
- ArgoCD
- Vault
If they were disabled in earlier milestones, re-enable them now to ensure:

- Metrics are scraped
- Alerts are triggered
- Dashboards show complete data

#### Validation Checklist
- All Grafana dashboards load successfully
- Prometheus targets are UP
- Loki logs visible for application
- Alerts appear in Alertmanager UI
- Slack receives alert notifications
- Restart alerts trigger on pod restarts

Wherer to access the prometehus,grafana ,alertmanager argocd,vault,application,loki gateway etc prober blackbox with portnumbers




