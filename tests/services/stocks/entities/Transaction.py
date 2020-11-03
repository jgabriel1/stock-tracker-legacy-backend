from pydantic import BaseModel


class Transaction(BaseModel):
    ticker: str
    quantity: int
    total_value: float
    timestamp: int = None
    average_price: float = None
