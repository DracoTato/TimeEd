import pytest
from dotenv import load_dotenv
from click.testing import CliRunner

from app import create_app
from app.db import db

load_dotenv()  # Load env variables (needed for some tests)


@pytest.fixture
def app():
    app = create_app({"ENV": "testing"})
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner():
    runner = CliRunner()
    return runner
