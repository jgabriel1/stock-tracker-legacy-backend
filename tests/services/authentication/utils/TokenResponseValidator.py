from pydantic import DictError
from requests import Response

from ..schemas import TokenResponseSchema


class TokenResponseValidator:
    response: Response

    def __init__(self, response: Response):
        self.response = response

    def validate(self) -> bool:
        data = self.response.json()
        try:
            TokenResponseSchema.validate(data)
            return True
        except DictError:
            return False
