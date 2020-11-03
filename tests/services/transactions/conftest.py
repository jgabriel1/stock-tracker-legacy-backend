from typing import List

import pytest


@pytest.fixture(scope='module')
def ticker() -> str:
    return 'AAPL'


@pytest.fixture(scope='module')
def transaction_data(ticker) -> dict:
    return {
        'ticker': ticker,
        'quantity': 100,
        'total_value': 44500,
    }


@pytest.fixture(scope='module')
def transactions_data(ticker) -> List[dict]:
    return [
        {
            'ticker': ticker,
            'quantity': 100,
            'total_value': 44500,
        },
        {
            'ticker': ticker,
            'quantity': -50,
            'total_value': -22250,
        },
        {
            'ticker': ticker,
            'quantity': 150,
            'total_value': 66750,
        },
    ]
