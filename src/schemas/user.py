import uuid

from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserSchema(BaseUserSchema):
    hashed_password: bytes | str  # ставить что-то одно и

    class Config:
        strict = True
        from_attributes = True


class UserRead(BaseUserSchema):
    logged_in_at: int  # поменять на время
