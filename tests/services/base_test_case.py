from starlette.testclient import TestClient


class BaseTestCase:
    __test__ = False

    client: TestClient
    user_data: dict
    token: str

    def __init__(self, client: TestClient, user_data: dict):
        self.client = client
        self.user_data = user_data

    def register_user(self) -> None:
        self.client.post('auth/register', json=self.user_data)

    def authenticate_user(self) -> None:
        response = self.client.post('auth/token', data={
            'username': self.user_data.get('username'),
            'password': self.user_data.get('password'),
        })

        self.token = response.json().get('access_token')
