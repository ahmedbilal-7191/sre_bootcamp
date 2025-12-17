import logging
from flask import Flask, request, Response, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .extensions import db, migrate, ma, REQUEST_COUNT, REQUEST_LATENCY, get_prometheus_registry
from .logging_config import setup_logging
from .errors import register_error_handlers
from .routes import student_bp
from config import config
import os
import time


def create_app(config_name=None):
    setup_logging()
    app = Flask(__name__)
    # If running under Gunicorn, use its handlers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger.handlers:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
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
    
    @app.route("/healthcheck", methods=["GET"])
    def health_check_global():
        return jsonify({"status": "ok"}), 200

    # Register error handlers
    register_error_handlers(app)

    # if config_name == "development":
    #     with app.app_context():
    #         db.create_all()

    if app.config.get("AUTO_CREATE_TABLES"):
        with app.app_context():
            db.create_all()
    
    @app.before_request
    def suppress_log_for_probes():
        if request.path in ["/metrics", "/healthcheck"]:
            logging.getLogger("werkzeug").disabled = True

        if request.path != "/metrics":
            request._start_time = time.time()

    @app.after_request
    def record_metrics(response):
        # Restore logging
        logging.getLogger("werkzeug").disabled = False

        # Skip for health + metrics
        if request.path in ["/metrics", "/healthcheck"]:
            return response

        method = request.method
        endpoint = request.path
        status = response.status_code

        REQUEST_COUNT.labels(
            method=method, endpoint=endpoint, http_status=status
        ).inc()

        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time
            REQUEST_LATENCY.labels(
                method=method, endpoint=endpoint, http_status=status
            ).observe(duration)

        return response

    # Expose metrics endpoint
    @app.route("/metrics")
    def metrics():
        # return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
        # IF USING GUNICORN
        registry = get_prometheus_registry()
        data = generate_latest(registry)
        # IF USING FLASK SERVER
        # data = generate_latest(REGISTRY)
        return Response(data, mimetype=CONTENT_TYPE_LATEST)

    return app
