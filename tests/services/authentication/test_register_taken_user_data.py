import pytest
from starlette.testclient import TestClient
from starlette.status import HTTP_409_CONFLICT


class RegisterWithTakenUserDataCase:

    def __init__(self, client: TestClient, user_data: dict):
        self.client = client
        self.user_data = user_data

        # Register user_data user:
        self.client.post('auth/register', json={
            **self.user_data,
        })

    def try_to_register_with_same_username(self):
        return self.client.post('auth/register', json={
            **self.user_data,
            'email': 'different_email@email.com',
        })

    def try_to_register_with_same_email(self):
        return self.client.post('auth/register', json={
            **self.user_data,
            'username': 'different_username',
        })


@pytest.fixture(scope='function')
def case(client: TestClient, user_data: dict):
    return RegisterWithTakenUserDataCase(client, user_data)


def test_not_allowed_to_register_with_same_username(case):
    response = case.try_to_register_with_same_username()
    assert response.status_code == HTTP_409_CONFLICT


def test_not_allowed_to_register_with_same_email(case):
    response = case.try_to_register_with_same_email()
    assert response.status_code == HTTP_409_CONFLICT
