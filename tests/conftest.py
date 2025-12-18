import pytest
from app import create_app
from app.extensions import db
from app.models.student import Student
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture
def app():
    app = create_app("testing")  # adding a "testing" config with SQLite in-memory in hte main app
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    """Provide a fresh database session for direct service tests."""
    return db.session
