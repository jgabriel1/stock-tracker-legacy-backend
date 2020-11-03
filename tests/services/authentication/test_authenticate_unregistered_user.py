import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_401_UNAUTHORIZED


class AuthenticateUnregisteredUserCase:

    def __init__(self, client: TestClient, user_data: dict):
        self.client = client
        self.user_data = user_data

    def try_to_authenticate(self):
        return self.client.post('auth/token', data={
            'username': self.user_data.get('username'),
            'password': self.user_data.get('password'),
        })


@pytest.fixture(scope='module')
def case(client: TestClient, user_data: dict):
    return AuthenticateUnregisteredUserCase(client, user_data)


def test_authenticate_unregistered_user(case: AuthenticateUnregisteredUserCase):
    token_response = case.try_to_authenticate()

    assert token_response.status_code == HTTP_401_UNAUTHORIZED
