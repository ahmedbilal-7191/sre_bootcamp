from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from prometheus_client import Counter, Histogram, CollectorRegistry, multiprocess
import os
ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()

# Prometheus RED metrics Using 0.5 in aws
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint', 'http_status'],
    buckets=[0.1, 0.3, 0.5, 1, 2, 5]
)


# Multiprocess registry (for Gunicorn) ---
def get_prometheus_registry():
    """Return a registry that aggregates metrics from all Gunicorn workers."""
    registry = CollectorRegistry()
    if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
        multiprocess.MultiProcessCollector(registry)
    return registry
