from typing import Mapping, Optional

from pydantic import ValidationError
from requests import Response

from ..entities import Stock
from ..schemas import StocksResponseSchema


class StocksResponseParser:
    response: Response

    def __init__(self, response: Response):
        self.response = response

    def get_parsed(self) -> Optional[Mapping[str, Stock]]:
        try:
            parsed = StocksResponseSchema.parse_raw(
                self.response.content
            )
            return parsed.stocks
        except ValidationError:
            raise ValueError('Response has wrong format.')
