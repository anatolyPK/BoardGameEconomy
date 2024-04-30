from fastapi import APIRouter, Depends

from ..models.base import User
from ..schemas.game import GameSearchSchema
from ..services.game import game_service
from ..utils.auth.manager import current_active_user


router = APIRouter(
    tags=['Game Search'],
)


@router.get("/game/search",
            response_model=GameSearchSchema)
async def game_search(game_name: str, user: User = Depends(current_active_user)):
    return await game_service.search_game(game_name=game_name)

