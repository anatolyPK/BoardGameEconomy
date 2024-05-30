import uuid
from datetime import datetime, date
from typing import Any, List

from sqlalchemy.types import JSON
from sqlalchemy import TIMESTAMP, func, String, ForeignKey, Boolean, Uuid
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    __abstarct__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

    type_annotation_map = {dict[str, Any]: JSON}

    repr_cols_num = 3
    repr_cols = []

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f'<{self.__class__.__name__} {", ".join(cols)}>'

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class User(Base):
    __tablename__ = "user"

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

    username: Mapped[str] = mapped_column(String(16), unique=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"))

    role: Mapped["Role"] = relationship(back_populates="users")
    game_transactions: Mapped[List["GameTransaction"]] = relationship(
        back_populates="user"
    )
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="rt_user"
    )
    # oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
    #     "OAuthAccount", lazy="joined"
    # )


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}  # < new

    name: Mapped[str] = mapped_column(String(16), unique=True)
    permission: Mapped[dict[str, Any]] = mapped_column(nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class Game(Base):
    __tablename__ = "game"

    bgg_id: Mapped[int] = mapped_column(unique=True)
    name_en: Mapped[str] = mapped_column(String(128))
    image: Mapped[str] = mapped_column(String(256), nullable=True)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)

    yearpublished: Mapped[int] = mapped_column(nullable=True)
    minplayers: Mapped[int] = mapped_column(nullable=True)
    maxplayers: Mapped[int] = mapped_column(nullable=True)
    playingtime: Mapped[int] = mapped_column(nullable=True)

    games_transactions: Mapped[List["GameTransaction"]] = relationship(
        back_populates="game"
    )
    names_ru_values: Mapped[List["GameRuName"]] = relationship(
        back_populates="base_game"
    )


class GameRuName(Base):
    __tablename__ = "game_ru_name"

    name_ru: Mapped[str] = mapped_column(String(128))
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))

    base_game: Mapped["Game"] = relationship(back_populates="names_ru_values")


class GameTransaction(Base):
    __tablename__ = "game_transaction"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id", ondelete="CASCADE"))

    purchase_date: Mapped[date]
    purchase_price: Mapped[float]

    selling_date: Mapped[date] = mapped_column(nullable=True)
    selling_price: Mapped[float] = mapped_column(nullable=True)

    description: Mapped[str] = mapped_column(String(128), nullable=True)

    user: Mapped["User"] = relationship(back_populates="game_transactions")
    game: Mapped["Game"] = relationship(back_populates="games_transactions")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    user_id: Mapped[Uuid] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    refresh_token: Mapped[str] = mapped_column(unique=True)
    fingerprint: Mapped[str] = mapped_column(String(250))
    should_deleted_at: Mapped[datetime]

    rt_user: Mapped["User"] = relationship(back_populates="refresh_tokens")
