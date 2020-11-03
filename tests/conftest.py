import pytest
from fastapi.testclient import TestClient

from server.api.dependencies import get_db
from server.main import app

from .settings.database import get_test_db, mongo_client


@pytest.fixture(scope='session', autouse=True)
def override_test_db():
    app.dependency_overrides[get_db] = get_test_db
    yield


@pytest.fixture(scope='module', autouse=True)
def reset_db():
    yield

    test_db = mongo_client.get_database()

    test_db.drop_collection('users')
    test_db.drop_collection('stocks')


@pytest.fixture(scope='session')
def client() -> TestClient:
    test_client = TestClient(app=app)
    return test_client


@pytest.fixture(scope='module')
def user_data() -> dict:
    return {
        'username': 'test_user',
        'password': 'password123',
        'email': 'test@email.com',
    }
