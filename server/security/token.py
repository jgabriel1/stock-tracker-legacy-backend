from datetime import datetime, timedelta

import jwt
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED

from ..settings.access_token import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    ALGORITHM,
    SECRET_KEY
)


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
) -> str:
    expire: datetime = datetime.utcnow() + expires_delta

    to_encode = data.copy()
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials.',
            headers={'WWW-Authenticate': 'Bearer'}
        )
