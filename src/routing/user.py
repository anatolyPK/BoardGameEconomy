from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from dependencies.user import get_current_active_user, get_current_token_payload
from schemas.user import UserSchema, UserRead


# для проверки только
http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(dependencies=[Depends(http_bearer)])


@router.get("/users/me", response_model=UserRead)
def user_check_self_info(
    user: UserSchema = Depends(get_current_active_user),
    payload: dict = Depends(get_current_token_payload),
):
    iat = payload.get("iat")

    return UserRead(**user.dict(), logged_in_at=iat)
