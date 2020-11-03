from pydantic import BaseModel


class Stock(BaseModel):
    ticker: str
    currently_owned_shares: int
    average_bought_price: float

    def is_empty(self) -> bool:
        return self.currently_owned_shares <= 0
