from typing import Optional

from pydantic import ValidationError
from requests import Response

from ..schemas import RegisterResponseSchema


class RegisterResponseParser:
    response: Response

    def __init__(self, response: Response):
        self.response = response

    def get_parsed(self) -> Optional[RegisterResponseSchema]:
        try:
            parsed = RegisterResponseSchema.parse_raw(
                self.response.content
            )
            return parsed
        except ValidationError:
            raise ValueError('Response has wrong format.')
