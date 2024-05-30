from sqlalchemy.exc import NoResultFound
from fastapi import APIRouter, Depends, HTTPException

from dependencies.user import get_current_active_user
from ..exceptions import UnauthorizedTransactionError
from ..schemas.transactions import (
    BaseGameTransactionSchema,
    GameAddTransactionSchema,
    GameTransactionPatchSchema,
    GameTransactionsSchema,
)
from ..services.game_transaction import game_transaction_service
from ..models.base import User


router = APIRouter(
    tags=["game transactions"],
)


@router.get("/transactions", response_model=GameTransactionsSchema)
async def games_transactions(user: User = Depends(get_current_active_user)):
    """
    Получение списка транзакций пользователя по настольным играм.

    Возвращает список транзакций в формате GameTransactionsSchema.
    """
    return await game_transaction_service.get_users_board_games_transactions(user=user)


@router.post("/", response_model=BaseGameTransactionSchema)
async def add_game(
    game: GameAddTransactionSchema, user: User = Depends(get_current_active_user)
):
    """
    Добавление новой транзакции по настольной игре.

    - **game**: Объект GameAddTransactionSchema - информация о добавляемой транзакции по игре

    Возвращает объект BaseGameTransactionSchema с информацией о добавленной транзакции.
    """
    return await game_transaction_service.add_game(game=game, user=user)


@router.patch("/games/{pk}", response_model=BaseGameTransactionSchema)
async def update_game_transaction(
    pk: int,
    transaction: GameTransactionPatchSchema,
    user: User = Depends(get_current_active_user),
):
    """
    Обновление информации о транзакции по настольной игре.

    - **pk**: Уникальный идентификатор транзакции.
    - **transaction**: Объект GameTransactionPatchSchema - данные для обновления транзакции.

    В случае успеха возвращает объект BaseGameTransactionSchema с обновленной информацией о транзакции.
    В случае если транзакция не найдена, возвращает ошибку с статусом 404 "Game transaction not found".
    В случае если транзакция не принадлежит пользователю, возвращает ошибку с статусом 404
    """
    try:
        return await game_transaction_service.update_transaction(transaction, user, pk)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Game transaction not found")
    except UnauthorizedTransactionError as ex:
        raise HTTPException(status_code=404, detail=ex.message)


@router.delete("/games/{pk}")
async def delete_game_transaction(
    pk: int, user: User = Depends(get_current_active_user)
):
    """
    Удаление транзакции по настольной игре.

    - **pk**: Уникальный идентификатор транзакции для удаления.

    В случае успеха операция не возвращает содержимого.
    В случае если транзакция не найдена, возвращает ошибку с статусом 404 "Game transaction not found"
    """
    try:
        await game_transaction_service.delete_transaction(user, pk)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Game transaction not found")
    except UnauthorizedTransactionError as ex:
        raise HTTPException(status_code=404, detail=ex.message)
