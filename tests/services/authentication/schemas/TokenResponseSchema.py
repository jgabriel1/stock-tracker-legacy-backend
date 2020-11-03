from typing import Literal

from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
    token_type: Literal['bearer']
    access_token: str
