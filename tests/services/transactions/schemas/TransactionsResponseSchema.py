from typing import List

from pydantic import BaseModel

from ..entities import Transaction


class TransactionsResponseSchema(BaseModel):
    transactions: List[Transaction]