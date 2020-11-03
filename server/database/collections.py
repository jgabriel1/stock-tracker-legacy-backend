from pymongo import DESCENDING, IndexModel
from pymongo.client_session import ClientSession
from pymongo.database import Collection, Database


def get_users_collection(session: ClientSession) -> Collection:
    db: Database = session.client.get_database()
    users: Collection = db.users

    if 'users' not in db.list_collection_names():
        users.create_indexes([
            # Unique constraint on username:
            IndexModel([('username', DESCENDING)], unique=True),

            # Unique constraint on email:
            IndexModel([('email', DESCENDING)], unique=True)
        ])

    return users
