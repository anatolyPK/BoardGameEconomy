from fastapi import APIRouter

from .auth import router as auth
from .general_stats import router as general_stats
from .game_transactions import router as games_transactions
from .games import router as game


router = APIRouter()


def get_apps_router():
    routes = (auth, general_stats, game, games_transactions)
    [router.include_router(route) for route in routes]
    return router
