from dataclasses import dataclass


@dataclass
class UserDTO:
    _id: str
    username: str
    password: str
    email: str