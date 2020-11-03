import os
from typing import Dict, List

import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND

load_dotenv()

BASE_URL = os.getenv('YAHOO_API_URL')


class YahooStockModel(BaseModel):
    symbol: str
    currency: str
    regularMarketPrice: float
    chartPreviousClose: float

    @classmethod
    def serialize_stock(cls, response_json: dict):
        serialized = response_json \
            .get('response')[0]    \
            .get('meta')           \

        return cls.parse_obj(serialized)


def get_stock_info(ticker_list: List[str]) -> Dict[str, YahooStockModel]:
    if not ticker_list:
        return {}

    query = {
        'symbols': ','.join(ticker_list),
        'range': '1d',
        'interval': '1d'
    }

    response = requests.get(BASE_URL, params=query)

    if not response.ok:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Yahoo Finance is currently unavailable.'
        )

    stocks_list = [
        YahooStockModel.serialize_stock(stock)
        for stock in response.json().get('spark').get('result')
    ]

    return {stock.symbol.upper(): stock for stock in stocks_list}
