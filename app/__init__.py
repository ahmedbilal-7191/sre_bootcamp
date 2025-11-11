from flask import Flask, request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .extensions import db, migrate, ma,REQUEST_COUNT, REQUEST_LATENCY, get_prometheus_registry
from .logging_config import setup_logging
from .errors import register_error_handlers
from .routes import student_bp
from config import config
# from ..config import config
# from dotenv import load_dotenv
# load_dotenv()
import os, time

def create_app(config_name=None):
    setup_logging()
    app = Flask(__name__)

    # Determine environment
    if not config_name:
        config_name = os.environ.get("FLASK_ENV", "default")
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Import models so Alembic sees them
    from app.models.student import Student

    # Register blueprints
    app.register_blueprint(student_bp)

    # Register error handlers
    register_error_handlers(app)

    # if config_name == "development":
    #     with app.app_context():
    #         db.create_all()

    if app.config.get("AUTO_CREATE_TABLES"):
        with app.app_context():
            db.create_all()

    # ============================
    #   PROMETHEUS INSTRUMENTATION
    # ============================
    @app.before_request
    def start_timer():
        # Skip metrics for /metrics endpoint itself
        if request.path == "/metrics":
            return
        request._start_time = time.time()

    @app.after_request
    def record_metrics(response):
        if request.path == "/metrics":
            return response
        method = request.method
        endpoint = request.path
        status_code = response.status_code

        # Count request
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()

        # Measure duration
        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint, http_status=status_code).observe(duration)

        return response

    # Expose metrics endpoint
    @app.route("/metrics")
    def metrics():
        # return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
        registry = get_prometheus_registry()
        data = generate_latest(registry)
        return Response(data, mimetype=CONTENT_TYPE_LATEST)

    return app
