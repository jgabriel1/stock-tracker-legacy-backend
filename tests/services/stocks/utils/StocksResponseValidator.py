from pydantic import DictError
from requests import Response

from ..schemas import StocksResponseSchema


class StocksResponseValidator:
    response: Response

    def __init__(self, response: Response):
        self.response = response

    def validate(self) -> bool:
        data = self.response.json()
        try:
            StocksResponseSchema.validate(data)
            return True
        except DictError:
            return False
