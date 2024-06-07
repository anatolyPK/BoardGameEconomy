import logging

from fastapi import Depends

from config.project_config import settings
from dependencies.auth import (
    extract_refresh_token_from_cookie,
    get_current_token_payload,
)
from schemas.user import UserInfoFromPayload, UserSchema
from services.user import user_service
from utils.jwt import validate_token_type
from utils.users import check_user_status


logger = logging.getLogger("debug")


async def get_current_user_from_access_token_payload(
    user_info: UserInfoFromPayload = Depends(get_current_token_payload),
) -> UserInfoFromPayload:
    validate_token_type(user_info.token_type, settings.auth_jwt.ACCESS_TOKEN_TYPE)
    return user_info


async def get_current_user_for_refresh(
    refresh_token_from_cookie: str = Depends(extract_refresh_token_from_cookie),
) -> UserSchema:
    user_info: UserInfoFromPayload = await get_current_token_payload(
        refresh_token_from_cookie
    )
    validate_token_type(user_info.token_type, settings.auth_jwt.REFRESH_TOKEN_TYPE)
    return await user_service.get_user(id=user_info.id)


async def get_current_active_user(
    user: UserInfoFromPayload = Depends(get_current_user_from_access_token_payload),
) -> UserInfoFromPayload:
    return await check_user_status(user, "User inactive", "is_active")


async def get_current_verified_user(
    user: UserInfoFromPayload = Depends(get_current_user_from_access_token_payload),
) -> UserInfoFromPayload:
    return await check_user_status(user, "User is not verified", "is_verified")


async def get_current_superuser(
    user: UserInfoFromPayload = Depends(get_current_user_from_access_token_payload),
) -> UserInfoFromPayload:
    return await check_user_status(user, "User is not superuser", "is_superuser")
