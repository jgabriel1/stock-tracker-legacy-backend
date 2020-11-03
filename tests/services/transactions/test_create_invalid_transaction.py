import pytest
from requests import Response
from starlette.testclient import TestClient
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from ..base_test_case import BaseTestCase


class CreateInvalidTransactionCase(BaseTestCase):
    """
    This will basically try to create a transaction selling more stocks than
    the amount of shares they currently own of a specific stock.
    """

    buying_transaction: dict
    selling_transaction: dict

    def __init__(
            self,
            client: TestClient,
            user_data: dict,
            buying_transaction: dict,
            selling_transaction: dict,
    ) -> None:
        super().__init__(client, user_data)

        self.buying_transaction = buying_transaction
        self.selling_transaction = selling_transaction

    def create_buying_transaction(self) -> Response:
        return self.client.post(
            'transactions',
            json=self.buying_transaction,
            headers={'Authorization': f'Bearer {self.token}'}
        )

    def create_selling_transaction(self) -> Response:
        return self.client.post(
            'transactions',
            json=self.selling_transaction,
            headers={'Authorization': f'Bearer {self.token}'}
        )


@pytest.fixture(scope='module')
def buying_transaction():
    return {
        'ticker': 'AAPL',
        'quantity': 100,
        'total_value': 44500,
    }


@pytest.fixture(scope='module')
def selling_transaction():
    return {
        'ticker': 'AAPL',
        'quantity': -120,
        'total_value': -53400,
    }


@pytest.fixture(scope='module')
def case(client, user_data, buying_transaction, selling_transaction):
    case = CreateInvalidTransactionCase(
        client,
        user_data,
        buying_transaction,
        selling_transaction,
    )

    case.register_user()
    case.authenticate_user()

    yield case


@pytest.fixture(scope='module')
def buying_transaction_response(case) -> Response:
    return case.create_buying_transaction()


def test_first_transaction_was_successful(buying_transaction_response):
    assert buying_transaction_response.status_code == HTTP_204_NO_CONTENT
    assert not buying_transaction_response.content


@pytest.fixture(scope='module')
def selling_transaction_response(case) -> Response:
    return case.create_selling_transaction()


def test_second_transaction_is_greater_than_the_first(
        buying_transaction,
        selling_transaction,
):
    bought_quantity: int = buying_transaction.get('quantity')
    sold_quantity: int = selling_transaction.get('quantity')

    assert bought_quantity >= 0
    assert sold_quantity <= 0

    assert abs(sold_quantity) > abs(bought_quantity)


def test_second_transaction_was_rejected(selling_transaction_response):
    assert selling_transaction_response.status_code == HTTP_400_BAD_REQUEST


def test_second_transaction_rejection_message(selling_transaction_response):
    assert selling_transaction_response.json() == {
        'detail': 'Cannot sell more stocks than you own!'
    }
