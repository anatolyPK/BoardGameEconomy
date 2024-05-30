from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from config.project_config import settings
from dependencies.auth import extract_refresh_token_from_cookie
from schemas.user import UserSchema
from services.user import user_service
from utils.auth import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token error"
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(settings.auth_jwt.TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
    )


async def get_user_by_token_sub(payload: dict) -> UserSchema:
    user_id = payload.get("sub")
    if user := await user_service.get_user(id=user_id):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid"
    )


async def get_current_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload, settings.auth_jwt.ACCESS_TOKEN_TYPE)
    return await get_user_by_token_sub(payload)


async def get_current_user_for_refresh(
    refresh_token_from_cookie: str = Depends(extract_refresh_token_from_cookie),
) -> UserSchema:
    payload = await get_current_token_payload(refresh_token_from_cookie)
    validate_token_type(payload, settings.auth_jwt.REFRESH_TOKEN_TYPE)

    return await get_user_by_token_sub(payload)


async def check_user_status(
    user: UserSchema, error_message: str, attribute: str
) -> UserSchema:
    if getattr(user, attribute):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)


async def get_current_active_user(
    user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    return await check_user_status(user, "User inactive", "is_active")


async def get_current_verified_user(
    user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    return await check_user_status(user, "User is not verified", "is_verified")


async def get_current_superuser(
    user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    return await check_user_status(user, "User is not superuser", "is_superuser")
