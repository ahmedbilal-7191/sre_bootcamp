from flask import Flask
from .extensions import db, migrate, ma
from .logging_config import setup_logging
from .errors import register_error_handlers
from .routes import student_bp
from config import config
# from ..config import config
# from dotenv import load_dotenv
# load_dotenv()
import os

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

    return app
