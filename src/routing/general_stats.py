from fastapi import APIRouter, Depends


from ..schemas.portfolio import GeneralInfoSchema
from ..services.game_transaction import game_transaction_service
from ..models.base import User
from ..utils.auth.manager import current_active_user


router = APIRouter(
    tags=['stats'],
)


@router.get("/",
            response_model=GeneralInfoSchema)
async def general_stats(user: User = Depends(current_active_user)):
    """
    Get general user stats

    - **user**: Auto-detected user object obtained via API token.

    Returns a GeneralInfoSchema object with details like total spent, avg spent, etc.
    """
    return await game_transaction_service.get_users_game_info(user)


@router.get("/info")
async def extended_stats(user: User = Depends(current_active_user)):
    """
    Get extended user stats

    This endpoint is under development and will provide detailed statistics
    regarding the user's purchases and sales of board games.

    Returns an info placeholder for now.
    """
    return {'info': "route in progress"}
