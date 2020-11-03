from server.repositories.users.dto import UserDTO
from pymongo.client_session import ClientSession as Session
from pymongo.database import Collection


class UsersRepository:
    session: Session
    collection: Collection

    def __init__(self, session: Session) -> None:
        self.session = session
        self.collection = session.client["users"]

    def create(self, username: str, password: str, email: str) -> UserDTO:
        result = self.collection.insert_one(
            {
                "username": username,
                "email": email,
                "password": password,
                "transactions": [],
            },
            session=self.session,
        )

        user = UserDTO(
            _id=result.inserted_id,
            username=username,
            email=email,
            password=password,
        )

        del user.password

        return user

    async def find_by_name(self, username: str) -> UserDTO:
        ...

    async def find_by_id(self, user_id: str) -> UserDTO:
        ...
