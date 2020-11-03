from typing import List, Optional

from requests import Response
from pydantic import ValidationError

from ..schemas import TransactionsResponseSchema
from ..entities import Transaction


class TransactionsResponseParser:
    response: Response

    def __init__(self, response: Response):
        self.response = response

    def get_parsed(self) -> Optional[List[Transaction]]:
        try:
            parsed = TransactionsResponseSchema.parse_raw(
                self.response.content
            )
            return parsed.transactions
        except ValidationError:
            raise ValueError('Response has wrong format.')
