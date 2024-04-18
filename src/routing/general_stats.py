from fastapi import APIRouter, Depends


from schemas.portfolio import GeneralInfo
from src.models.base import User
from utils.auth.manager import current_active_user


router = APIRouter(
    tags=['General Stats'],
)


@router.get("/",
            response_model=GeneralInfo)
async def crypto_portfolio(user: User = Depends(current_active_user)):
    return {'message': 'hello'}
    # return await crypto_service.get_user_portfolio(user)

