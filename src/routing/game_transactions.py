from sqlalchemy.exc import NoResultFound
from fastapi import APIRouter, Depends, HTTPException

from ..exceptions import UnauthorizedTransactionError
from ..schemas.transactions import BaseGameTransactionSchema, GameAddTransactionSchema, GameTransactionPatchSchema, GameTransactionsSchema
from ..services.game_transaction import game_transaction_service
from ..models.base import User
from ..utils.auth.manager import current_active_user


router = APIRouter(
    tags=['Board Game Transactions'],
)


@router.get("/transactions",
            response_model=GameTransactionsSchema)
async def games_transactions(user: User = Depends(current_active_user)):
    return await game_transaction_service.get_users_board_games_transactions(user=user)


@router.post("/",
             response_model=BaseGameTransactionSchema)
async def add_game(game: GameAddTransactionSchema,
                   user: User = Depends(current_active_user)):
    return await game_transaction_service.add_game(game=game, user=user)


@router.patch("/games/{pk}",
              response_model=BaseGameTransactionSchema)
async def update_game_transaction(pk: int,
                                  transaction: GameTransactionPatchSchema,
                                  user: User = Depends(current_active_user),
                                  ):
    try:
        return await game_transaction_service.update_transaction(transaction, user, pk)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Game transaction not found")
    except UnauthorizedTransactionError as ex:
        raise HTTPException(status_code=404, detail=ex.message)


@router.delete("/games/{pk}")
async def delete_game_transaction(pk: int,
                                  user: User = Depends(current_active_user)):
    try:
        await game_transaction_service.delete_transaction(user, pk)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Game transaction not found")
    except UnauthorizedTransactionError as ex:
        raise HTTPException(status_code=404, detail=ex.message)