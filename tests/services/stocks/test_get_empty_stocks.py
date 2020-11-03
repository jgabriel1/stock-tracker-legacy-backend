import pytest
from requests import Response
from starlette.status import HTTP_200_OK

from ..base_test_case import BaseTestCase


class GetEmptyStocksCase(BaseTestCase):
    """
    This will attempt to get stocks data without even having made a
    transaction before.
    """

    def get_stocks(self) -> Response:
        return self.client.get('stocks', headers={
            'Authorization': f'Bearer {self.token}'
        })


@pytest.fixture(scope='module')
def case(client, user_data):
    case = GetEmptyStocksCase(client, user_data)

    case.register_user()
    case.authenticate_user()
    return case


@pytest.fixture(scope='module')
def get_stocks_response(case) -> Response:
    return case.get_stocks()


def test_response_status_is_ok(get_stocks_response):
    assert get_stocks_response.status_code == HTTP_200_OK


def test_response_data_is_empty(get_stocks_response):
    assert get_stocks_response.json() == {
        'stocks': {}
    }
