from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class Transaction(BaseModel):
    ticker: str
    quantity: int
    total_value: float

    timestamp: int = None
    average_price: float = None

    @validator('ticker', always=True)
    def uppercase_ticker(cls, value: str, **kwargs):
        return value if value.isupper() else value.upper()

    @validator('timestamp', always=True)
    def snap_current_time(cls, value: int, **kwargs):
        return value or datetime.utcnow().timestamp()

    @validator('average_price', always=True)
    def calculate_average_price(cls, value: float, values: dict, **kwargs):
        return value or values.get('total_value') / values.get('quantity')


class TransactionHistory(BaseModel):
    transactions: List[Transaction]
