from typing import List, Iterator

import pytest
from requests import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from starlette.testclient import TestClient

from .utils import (
    StocksResponseValidator,
    StocksResponseParser,
    StocksDataCalculator,
    TransactionListParser,
)
from ..base_test_case import BaseTestCase


class GetStocksCase(BaseTestCase):
    transactions_data: List[dict]

    def __init__(
            self,
            client: TestClient,
            user_data: dict,
            transactions_data: List[dict]
    ):
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

    def get_stocks(self) -> Response:
        return self.client.get('stocks', headers={
            'Authorization': f'Bearer {self.token}'
        })


@pytest.fixture(scope='module')
def case(client, user_data, transactions_data):
    case = GetStocksCase(client, user_data, transactions_data)

    case.register_user()
    case.authenticate_user()

    return case


@pytest.fixture(scope='module')
def get_stocks_response(case):
    return case.get_stocks()


@pytest.fixture(scope='function')
def stocks_response_validator(get_stocks_response):
    return StocksResponseValidator(get_stocks_response)


@pytest.fixture(scope='module')
def stocks_response_parser(get_stocks_response):
    return StocksResponseParser(get_stocks_response)


@pytest.fixture(scope='module')
def stocks_data_calculator(transactions_data):
    transactions_parser = TransactionListParser(transactions_data)
    return StocksDataCalculator(transactions_parser.get_parsed())


def test_all_transactions_were_accepted(case):
    for response in case.create_transactions():
        assert response.status_code == HTTP_204_NO_CONTENT


def test_get_socks_status_code(get_stocks_response):
    assert get_stocks_response.status_code == HTTP_200_OK


def test_get_stocks_response_format(stocks_response_validator):
    assert stocks_response_validator.validate()


def test_get_stocks_response_data_is_correct(
        stocks_response_parser,
        stocks_data_calculator,
):
    recieved_stocks_data = stocks_response_parser.get_parsed()
    expected_stocks_data = stocks_data_calculator.calculate_stocks()

    assert recieved_stocks_data == expected_stocks_data
