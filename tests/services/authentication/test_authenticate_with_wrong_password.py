import pytest
from starlette.testclient import TestClient
from starlette.status import HTTP_401_UNAUTHORIZED


class AuthenticateWrongPasswordCase:

    def __init__(self, client: TestClient, user_data: dict):
        self.client = client
        self.user_data = user_data

        # Register user with a certain password:
        self.client.post('auth/register', json={
            **user_data,
            'password': 'password123'
        })

    def try_to_authenticate(self):
        # Use a different password when trying to authenticate
        return self.client.post('auth/token', data={
            'username': self.user_data.get('username'),
            'password': 'password321',
        })


@pytest.fixture(scope='module')
def case(client: TestClient, user_data: dict):
    return AuthenticateWrongPasswordCase(client, user_data)


def test_that_user_request_gets_refused(case: AuthenticateWrongPasswordCase):
    response = case.try_to_authenticate()

    assert response.status_code == HTTP_401_UNAUTHORIZED
