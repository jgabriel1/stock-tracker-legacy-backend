import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from requests import Response
from .utils import (
    AuthTokenValidator,
    TokenResponseParser,
    TokenResponseValidator
)


class AuthenticateUserCase:

    def __init__(self, client: TestClient, user_data: dict) -> None:
        self.client = client
        self.user_data = user_data

    def register_user(self) -> Response:
        return self.client.post('auth/register', json=self.user_data)

    def authenticate_user(self) -> Response:
        return self.client.post('auth/token', data={
            'username': self.user_data.get('username'),
            'password': self.user_data.get('password'),
        })


@pytest.fixture(scope='module')
def case(client: TestClient, user_data: dict):
    return AuthenticateUserCase(client, user_data)


@pytest.fixture(scope='module')
def register_response(case):
    return case.register_user()


@pytest.fixture(scope='module')
def token_response(case):
    return case.authenticate_user()


@pytest.fixture(scope='module')
def token_response_validator(token_response):
    return TokenResponseValidator(token_response)


@pytest.fixture(scope='module')
def access_token(token_response):
    parser = TokenResponseParser(token_response)
    return parser.get_parsed().access_token


@pytest.fixture(scope='function')
def token_validator(access_token):
    return AuthTokenValidator(access_token)


def test_user_was_registered(register_response):
    assert register_response.status_code == HTTP_201_CREATED


def test_token_request_was_successful(token_response):
    assert token_response.status_code == HTTP_200_OK


def test_token_response_format_is_correct(token_response_validator):
    assert token_response_validator.validate()


def test_token_is_valid(token_validator):
    assert token_validator.validate()
