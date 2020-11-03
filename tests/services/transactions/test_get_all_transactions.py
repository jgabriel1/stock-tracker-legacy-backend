from typing import List, Iterator

import pytest
from requests import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from .utils import TransactionsResponseParser, TransactionsResponseValidator
from ..base_test_case import BaseTestCase


class ListTransactionsCase(BaseTestCase):
    transactions_data: List[dict]

    def __init__(self, client, user_data, transactions_data: List[dict]):
        super().__init__(client, user_data)
        self.transactions_data = transactions_data

    def create_transactions(self) -> Iterator[Response]:
        for transaction in self.transactions_data:
            yield self.client.post(
                'transactions',
                json=transaction,
                headers={
                    'Authorization': f'Bearer {self.token}'
                }
            )

    def fetch_all_transactions(self, ticker: str) -> Response:
        return self.client.get(
            'transactions',
            headers={'Authorization': f'Bearer {self.token}'},
            params={'ticker': ticker}
        )


@pytest.fixture(scope='module')
def case(client, user_data, transactions_data):
    case = ListTransactionsCase(client, user_data, transactions_data)

    case.register_user()
    case.authenticate_user()

    return case


def test_all_transactions_were_accepted(case):
    for response in case.create_transactions():
        assert response.status_code == HTTP_204_NO_CONTENT


@pytest.fixture(scope='module')
def transactions_response(case, ticker) -> Response:
    return case.fetch_all_transactions(ticker)


def test_response_is_successful(transactions_response):
    assert transactions_response.status_code == HTTP_200_OK


@pytest.fixture(scope='function')
def transactions_response_validator(transactions_response):
    return TransactionsResponseValidator(transactions_response)


def test_response_data_format_is_correct(transactions_response_validator):
    assert transactions_response_validator.validate()


@pytest.fixture(scope='function')
def transactions_response_parser(transactions_response):
    return TransactionsResponseParser(transactions_response)


def test_transactions_are_the_same_created(
        transactions_response_parser,
        transactions_data,
):
    transactions_recieved = transactions_response_parser.get_parsed()

    for created, recieved in zip(transactions_data, reversed(transactions_recieved)):
        assert created.get('ticker') == recieved.ticker
        assert created.get('quantity') == recieved.quantity
        assert created.get('total_value') == recieved.total_value
