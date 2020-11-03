from typing import Mapping

from pydantic import BaseModel

from ..entities import Stock


class StocksResponseSchema(BaseModel):
    stocks: Mapping[str, Stock]
