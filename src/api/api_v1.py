from fastapi import APIRouter

from auth.routes import router as auth
from users.routes import router as user
from routing.general_stats import router as general_stats
from routing.game_transactions import router as games_transactions
from routing.games import router as game


router = APIRouter(
    prefix="/api/v1"
)


def get_apps_router():
    routes = (auth, general_stats, game, games_transactions, user)
    [router.include_router(route) for route in routes]
    return router
