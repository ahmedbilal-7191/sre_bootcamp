import os

basedir = os.path.abspath(os.path.dirname(__file__))

def build_db_uri(driver="psycopg2"):
    user = os.environ.get("POSTGRES_USER", "user")
    password = os.environ.get("POSTGRES_PASSWORD", "password")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "default_db")

    return f"postgresql+{driver}://{user}:{password}@{host}:{port}/{db}"

class Config:
    """Base config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    DEBUG = False
    TESTING = False
    AUTO_CREATE_TABLES = False
    SQLALCHEMY_DATABASE_URI = build_db_uri()

class DevelopmentConfig(Config):
    DEBUG = True
    AUTO_CREATE_TABLES = True

class StagingConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # SECRET_KEY = "test-secret-key"

class ProductionConfig(Config):
    DEBUG = False

# Mapping for easy access
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
