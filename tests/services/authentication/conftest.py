import pytest


@pytest.fixture(scope='module')
def user_data():
    """
    Simple user mock data.
    """
    yield {
        'username': 'test_username',
        'password': 'password123',
        'email': 'test@email.com',
    }
