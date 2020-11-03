import pytest
from requests import Response
from starlette.testclient import TestClient
from starlette.status import HTTP_204_NO_CONTENT

from ..base_test_case import BaseTestCase


class CreateNewTransactionCase(BaseTestCase):
    transaction_data: dict

    def __init__(self, client: TestClient, user_data: dict, transaction_data: dict):
        super().__init__(client, user_data)

        self.transaction_data = transaction_data

    def create_transaction(self) -> Response:
        return self.client.post(
            'transactions',
            json=self.transaction_data,
            headers={
                'Authorization': f'Bearer {self.token}'
            }
        )


@pytest.fixture(scope='module')
def case(client: TestClient, user_data: dict, transaction_data: dict):
    case = CreateNewTransactionCase(client, user_data, transaction_data)

    case.register_user()
    case.authenticate_user()

    return case


@pytest.fixture(scope='module')
def transaction_creation_response(case) -> Response:
    return case.create_transaction()


def test_response_status_code(transaction_creation_response):
    assert transaction_creation_response.status_code == HTTP_204_NO_CONTENT


def test_response_has_no_content(transaction_creation_response):
    assert not transaction_creation_response.content
