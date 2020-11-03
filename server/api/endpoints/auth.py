from fastapi import APIRouter, Depends, HTTPException
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT
)

from ...crud import crud_users
from ...models.user import User, UserInDB
from ...security.token import Token, create_access_token
from ..dependencies import get_db, get_current_authenticated_user

router = APIRouter()


@router.post('/register', status_code=HTTP_201_CREATED, response_model=User)
def register(user: UserInDB, session: ClientSession = Depends(get_db)):
    try:
        crud_users.create(user, session=session)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail='Username or email already taken!'
        )

    return user


@router.post('/token', response_model=Token)
def get_access_token(user: UserInDB = Depends(get_current_authenticated_user)):
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
