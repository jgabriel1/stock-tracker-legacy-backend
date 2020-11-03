import pytest
from requests import Response
from starlette.testclient import TestClient
from starlette.status import HTTP_201_CREATED

from .utils import RegisterResponseValidator, RegisterResponseParser


class RegisterUserCase:

    def __init__(self, client: TestClient, user_data: dict):
        self.client = client
        self.user_data = user_data

    def register(self) -> Response:
        return self.client.post('auth/register', json=self.user_data)


@pytest.fixture(scope='module')
def case(client: TestClient, user_data: dict) -> RegisterUserCase:
    return RegisterUserCase(client, user_data)


@pytest.fixture(scope='module')
def register_response(case):
    return case.register()


@pytest.fixture(scope='function')
def register_response_validator(register_response):
    return RegisterResponseValidator(register_response)


@pytest.fixture(scope='function')
def register_response_parser(register_response):
    return RegisterResponseParser(register_response)


def test_register_request_is_successful(register_response):
    assert register_response.status_code == HTTP_201_CREATED


def test_register_response_has_correct_format(register_response_validator):
    assert register_response_validator.validate()


def test_is_returning_user_data(register_response_parser, user_data):
    parsed = register_response_parser.get_parsed()

    username = parsed.username
    email = parsed.email

    assert username == user_data.get('username')
    assert email == user_data.get('email')
