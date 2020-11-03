from typing import Optional

from pydantic import ValidationError
from requests import Response

from ..schemas import TokenResponseSchema


class TokenResponseParser:
    response: Response

    def __init__(self, response: Response):
        self.response = response

    def get_parsed(self) -> Optional[TokenResponseSchema]:
        try:
            parsed = TokenResponseSchema.parse_raw(
                self.response.content
            )
            return parsed
        except ValidationError:
            raise ValueError('Response has wrong format.')