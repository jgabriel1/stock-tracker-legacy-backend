from typing import Dict

from pydantic import BaseModel, validator


class Stock(BaseModel):
    ticker: str
    total_invested: float
    total_sold: float
    currently_owned_shares: int
    average_bought_price: float

    @validator('ticker')
    def uppercase_ticker(cls, value: str):
        return value if value.isupper() else value.upper()


class StocksResponse(BaseModel):
    stocks: Dict[str, Stock]
