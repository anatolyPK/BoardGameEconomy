import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, field_validator

from config.project_config import settings


class AccessAndRefreshTokens(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class RefreshTokenCreate(BaseModel):
    user_id: uuid.UUID
    refresh_token: str
    fingerprint: str

    should_deleted_at: datetime | None

    @field_validator("should_deleted_at")
    @classmethod
    def set_should_deleted_at(cls, v):
        if v is None:
            refresh_token_expire_days = settings.auth_jwt.refresh_token_expire_days
            now = datetime.now(timezone.utc)
            expire = now + timedelta(days=refresh_token_expire_days)
            return expire.replace(tzinfo=None)
        return v


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreateSchemeForDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role_id: int = 2
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
