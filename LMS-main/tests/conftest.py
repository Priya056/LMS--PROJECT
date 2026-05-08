import os
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
import pytest
from app import app as flask_app
from models import db

@pytest.fixture(scope='session', autouse=True)
def app():
    # Set up application config for testing
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key",
        "LOGIN_DISABLED": False
    })
    # Mock any required environment variables
    os.environ["FLASK_SECRET_KEY"] = "test-secret-key"
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-key"

    with flask_app.app_context():
        # Create all tables before the test runs
        db.create_all()
        # Seed test database
        from seed import seed_database
        seed_database()
        
        yield flask_app
        # Drop all tables after the test runs
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
