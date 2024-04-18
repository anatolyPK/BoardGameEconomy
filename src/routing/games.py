from fastapi import APIRouter, Depends


from schemas.portfolio import GeneralInfo
from schemas.transactions import BaseGameTransaction, GameAddTransaction
from services.game_transaction import game_service
from src.models.base import User
from utils.auth.manager import current_active_user


router = APIRouter(
    tags=['General Stats'],
)


@router.post("/",
            response_model=BaseGameTransaction)
async def add_games(game: GameAddTransaction,
                    user: User = Depends(current_active_user)):
    return await game_service.add_game(game=game, user=user)
    # return await crypto_service.get_user_portfolio(user)

