from sqlalchemy import select, update

from models.base import RefreshToken
from schemas.auth import RefreshTokenCreate
from src.config.db.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository


class AuthRepository(SqlAlchemyRepository):
    async def put_or_refresh_refresh_token(self, refresh_token: RefreshTokenCreate):
        async with self._session() as session:
            stmt = select(self.model).filter_by(fingerprint=refresh_token.fingerprint)
            result = await session.execute(stmt)
            token_from_bd = result.scalar()

            if not token_from_bd:
                instance = self.model(**refresh_token.dict())
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance

            stmt = (
                update(self.model)
                .values(**refresh_token.dict())
                .where(self.model.id == token_from_bd.id)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()


auth_repository = AuthRepository(
    model=RefreshToken, db_session=db_helper.get_db_session_context
)
