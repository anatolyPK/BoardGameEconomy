from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.exc import NoResultFound

from dependencies.user import get_current_user_for_refresh, get_current_user
from schemas.user import UserSchema, BaseUserSchema
from dependencies.auth import (
    validate_auth_user,
    verify_fingerprint,
    create_tokens,
    extract_refresh_token_from_cookie,
)
from services.auth import auth_service
from services.user import user_service
from ..schemas.auth import AccessTokenInfo, UserCreate


router = APIRouter(
    tags=["auth"],
)


@router.post("/login", response_model=AccessTokenInfo)
async def auth_user_issue_jwt(
    response: Response,
    user: UserSchema = Depends(validate_auth_user),
    fingerprint: str = Depends(verify_fingerprint),
):
    tokens = await create_tokens(user=user, fingerprint=fingerprint)

    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)
    return AccessTokenInfo(access_token=tokens.access_token)


@router.post("/logout", status_code=200)
async def auth_user_logout(
    response: Response,
    user: UserSchema = Depends(get_current_user),
    refresh_token_from_cookie: str = Depends(extract_refresh_token_from_cookie),
    fingerprint: str = Depends(verify_fingerprint),
):
    """
    Клиентская сторона самостоятельно удаляет access_token из заголовка!
    """
    response.delete_cookie(key="refresh_token", httponly=True)
    await auth_service.delete_refresh_token(
        user=user, refresh_token=refresh_token_from_cookie, fingerprint=fingerprint
    )


@router.post("/refresh", response_model=AccessTokenInfo)
async def auth_refresh_jwt(
    response: Response,
    fingerprint: str = Depends(verify_fingerprint),
    refresh_token_from_cookie: str = Depends(extract_refresh_token_from_cookie),
    user: UserSchema = Depends(get_current_user_for_refresh),
):
    try:
        await auth_service.delete_refresh_token(
            user=user, refresh_token=refresh_token_from_cookie, fingerprint=fingerprint
        )
    except NoResultFound:  # продумать как обработать ошибки
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # исправить
            detail="Invalid username or password",  # добавить больше ошибок
        )
    tokens = await create_tokens(user=user, fingerprint=fingerprint)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)
    return AccessTokenInfo(access_token=tokens.access_token)


@router.post("/register", response_model=BaseUserSchema)
async def auth_register_user(
    user_data: UserCreate,
):
    created_user = await user_service.create_user(user_data)
    return created_user
