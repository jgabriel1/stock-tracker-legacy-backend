from typing import Optional

from pymongo.client_session import ClientSession

from ..database.collections import get_users_collection
from ..models.user import User, UserInDB
from ..security.hash import hash_password, verify_password


def create(user: UserInDB, session: ClientSession) -> None:
    users = get_users_collection(session=session)

    users.insert_one({
        'username': user.username,
        'email': user.email,
        'password': hash_password(user.password),
        'transactions': []
    }, session=session)


def show(username: str, session: ClientSession) -> Optional[UserInDB]:
    users = get_users_collection(session=session)

    user = users.find_one({'username': username}, session=session)
    if user is not None:
        return UserInDB.parse_obj(user)


def update_password(
    username: str, new_password: str, session: ClientSession
) -> None:
    users = get_users_collection(session=session)

    users.update_one(
        filter={'username': username},
        update={
            '$set': {'password': hash_password(new_password)}
        },
        session=session
    )


def destroy(username: str, session: ClientSession) -> None:
    users = get_users_collection(session=session)

    users.delete_one({'username': username}, session=session)


def authenticate(
    username: str, password: str, session: ClientSession
) -> Optional[User]:

    user = show(username, session=session)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None

    return user
