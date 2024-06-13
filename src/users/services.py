import uuid

from fastapi_mail import MessageSchema

from auth.schemas import NewUserPassword, UserCreate, UserCreateSchemeForDB
from core.config.email import fast_mail
from models.base import User
from schemas.user import UserSchema, UserUpdate, UserUpdateWithHashedPassword
from services.base import BaseService
from core.security import hash_password
from users.repository import user_repository


class UserService(BaseService):
    async def update(self, pk: uuid.UUID, new_user_data: UserUpdate) -> User:
        hashed_password = None
        if new_user_data.password is not None:
            hashed_password = hash_password(new_user_data.password)
        updated_date = UserUpdateWithHashedPassword(
            **new_user_data.dict(), hashed_password=hashed_password
        )
        return await self.repository.update(updated_date, id=pk)

    async def set_new_user_password(self, user: UserSchema, new_password: str):
        hashed_password = hash_password(new_password)
        update_data = NewUserPassword(hashed_password=str(hashed_password))
        await self.repository.update(update_data, id=user.id)

    async def get_user(  # REFACTOR
        self, email: str = None, id: str = None
    ) -> UserSchema:
        if email and (user := await self.repository.get_single(email=email)):
            return UserSchema.from_orm(user)
        elif id and (user := await self.repository.get_single(id=id)):
            return UserSchema.from_orm(user)

    async def create_user(self, user_data: UserCreate):
        users_data_for_db = self._convert_model_in_db_models(user_data)
        created_user = await self.repository.create(users_data_for_db)

        template = f"""<html>
           <body>
               <p>Для подтверждения вашей учетной записи, пройдите по следующей ссылке:</p>
               <a href='{1}'>Нажмите здесь, чтобы подтвердить</a>
           </body>
       </html>"""

        message = MessageSchema(
            subject="Подтверждение учетной записи",
            recipients=[user_data.email],
            body=template,
            subtype="html",
        )

        await fast_mail.send_message(
            message=message
        )
        return created_user

    @staticmethod
    def _convert_model_in_db_models(user_data: UserCreate) -> UserCreateSchemeForDB:
        user_data_dict = user_data.dict()
        user_password = user_data_dict.pop("password")
        user_hashed_password = hash_password(user_password).decode()
        return UserCreateSchemeForDB(
            **user_data_dict, hashed_password=user_hashed_password
        )


user_service = UserService(user_repository)
