import uuid

from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None

    class Config:
        from_attributes = True


class UserUpdateWithHashedPassword(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None


class BaseUserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserInfoFromPayload(BaseModel):
    token_type: str
    id: uuid.UUID
    exp: int
    iat: int
    username: str = None
    email: EmailStr = None
    is_superuser: bool = None
    is_verified: bool = None
    is_active: bool = None


class UserSchema(BaseUserSchema):
    hashed_password: bytes | str  # ставить что-то одно и

    class Config:
        strict = True
        from_attributes = True


class UserRead(BaseUserSchema):
    logged_in_at: int | None = None

    class Config:
        from_attributes = True
