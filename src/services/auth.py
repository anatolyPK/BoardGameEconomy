from repositories.auth import auth_repository
from schemas.auth import RefreshTokenCreate
from schemas.user import UserSchema
from services.base import BaseService


class AuthService(BaseService):
    async def put_refresh_token(
        self, user_data: UserSchema, refresh_token: str, fingerprint: str
    ):
        refresh_token_dto = RefreshTokenCreate(
            user_id=user_data.id,
            refresh_token=refresh_token,
            fingerprint=fingerprint,
            should_deleted_at=None,
        )
        await self.repository.create(refresh_token_dto)

    async def delete_refresh_token(
        self, user: UserSchema, refresh_token: str, fingerprint: str
    ):
        """
        При запросе к БД проверяет, что RT и FP принадлжат данному пользователю
        """
        await self.repository.delete(
            user_id=user.id, refresh_token=refresh_token, fingerprint=fingerprint
        )


auth_service = AuthService(auth_repository)
