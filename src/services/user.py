from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from repositories.user import user_repository
from schemas.auth import UserCreate, UserCreateSchemeForDB
from schemas.user import UserSchema
from services.base import BaseService
from utils.auth import hash_password


class UserService(BaseService):
    async def get_user(  # REFACTOR
        self, email: str = None, id: str = None
    ) -> UserSchema:
        if email and (user := await self.repository.get_single(email=email)):
            return UserSchema.from_orm(user)
        elif id and (user := await self.repository.get_single(id=id)):
            return UserSchema.from_orm(user)

    async def create_user(self, user_data: UserCreate):
        users_data_for_db = self._convert_model_in_db_models(user_data)
        try:
            return await self.repository.create(users_data_for_db)
        except IntegrityError as e:
            message = "A conflict occurred during the operation."
            if "unique constraint" in str(e.orig).lower():
                message = "A user with these details already exists."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)

    @staticmethod
    def _convert_model_in_db_models(user_data: UserCreate) -> UserCreateSchemeForDB:
        user_data_dict = user_data.dict()
        user_password = user_data_dict.pop("password")
        user_hashed_password = hash_password(user_password).decode()
        return UserCreateSchemeForDB(
            **user_data_dict, hashed_password=user_hashed_password
        )


user_service = UserService(user_repository)
