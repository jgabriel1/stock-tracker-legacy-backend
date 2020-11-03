from fastapi import APIRouter, Body, Depends, HTTPException, Response
from pymongo.client_session import ClientSession
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from ...crud import crud_users
from ...models.user import User
from ..dependencies import get_current_user, get_db

router = APIRouter()


@router.get('/users/me', response_model=User)
def show_info(user: User = Depends(get_current_user)):
    return user


@router.put('/users/password', status_code=HTTP_204_NO_CONTENT)
def change_password(
    current_password: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    user: User = Depends(get_current_user),
    session: ClientSession = Depends(get_db)
):
    with session.start_transaction():
        authenticated_user = crud_users.authenticate(
            user.username, current_password, session=session
        )

        if not authenticated_user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Cannot change password, wrong current password.'
            )

        crud_users.update_password(
            user.username, new_password, session=session
        )

    return Response(status_code=HTTP_204_NO_CONTENT)


@router.delete('/users', status_code=HTTP_204_NO_CONTENT)
def unregister(
    current_password: str = Body(..., embed=True),
    user: User = Depends(get_current_user),
    session: ClientSession = Depends(get_db)
):
    with session.start_transaction():
        authenticated_user = crud_users.authenticate(
            user.username, current_password, session=session
        )

        if not authenticated_user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Cannot unregister, wrong current password.'
            )

        crud_users.destroy(user.username, session=session)

    return Response(status_code=HTTP_204_NO_CONTENT)
