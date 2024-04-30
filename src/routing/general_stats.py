from fastapi import APIRouter, Depends


from ..schemas.portfolio import GeneralInfoSchema
from ..services.game_transaction import game_transaction_service
from ..models.base import User
from ..utils.auth.manager import current_active_user


router = APIRouter(
    tags=['Stats'],
)


@router.get("/",
            response_model=GeneralInfoSchema)
async def general_stats(user: User = Depends(current_active_user)):
    return await game_transaction_service.get_users_game_info(user)
