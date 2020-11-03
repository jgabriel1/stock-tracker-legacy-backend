from pydantic import BaseModel, EmailStr


class RegisterResponseSchema(BaseModel):
    username: str
    email: EmailStr
