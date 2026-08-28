import os

import pytest

from app import create_app
from app.data import QnaStore

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "qna")


@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True, QNA_DIR=os.path.abspath(FIXTURES_DIR))
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def store():
    return QnaStore(os.path.abspath(FIXTURES_DIR))
