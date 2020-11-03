import os

import jwt
from dotenv import load_dotenv


class AuthTokenValidator:
    token: str
    SECRET_KEY: str
    ALGORITHM: str

    def __init__(self, access_token: str):
        self.token = access_token

        load_dotenv()
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.ALGORITHM = os.getenv('ALGORITHM')

    def validate(self) -> bool:
        try:
            jwt.decode(
                jwt=self.token,
                key=self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
            return True
        except jwt.PyJWTError:
            return False
