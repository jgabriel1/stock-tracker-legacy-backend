from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo.client_session import ClientSession
from starlette.status import HTTP_401_UNAUTHORIZED

from ..crud import crud_users
from ..database.connection import client
from ..models.user import UserInDB
from ..security.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_db() -> ClientSession:
    with client.start_session() as session:
        yield session


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: ClientSession = Depends(get_db)
) -> Optional[UserInDB]:

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    payload = decode_token(token)

    username: str = payload.get('sub')
    if username is None:
        raise credentials_exception

    user = crud_users.show(username, session)
    if user is None:
        raise credentials_exception

    return UserInDB.parse_obj(user)


def get_current_authenticated_user(
    form: OAuth2PasswordRequestForm = Depends(),
    session: ClientSession = Depends(get_db)
) -> Optional[UserInDB]:
    user = crud_users.authenticate(
        form.username, form.password, session=session
    )

    return user
