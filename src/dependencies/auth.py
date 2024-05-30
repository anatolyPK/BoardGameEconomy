from typing import Annotated

from fastapi import Depends, HTTPException, Header, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from schemas.auth import AccessAndRefreshTokens
from schemas.user import UserSchema
from services.user import user_service
from utils.auth import validate_password, create_access_token, create_refresh_token


async def verify_fingerprint(x_device_fingerprint: str = Header(None)):
    if x_device_fingerprint is None:
        raise HTTPException(status_code=400, detail="Fingerprint header is missing")
    return x_device_fingerprint


async def extract_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")
    return refresh_token


async def create_tokens(user: UserSchema, fingerprint: str) -> AccessAndRefreshTokens:
    access_token: str = create_access_token(user)
    refresh_token: str = await create_refresh_token(user, fingerprint)
    return AccessAndRefreshTokens(
        access_token=access_token, refresh_token=refresh_token
    )


async def validate_auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    if not (user := await user_service.get_user(email=form_data.username)):
        raise unauthed_exc
    if not validate_password(
        password=form_data.password, hashed_password=user.hashed_password
    ):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User inactive"
        )
    return user
