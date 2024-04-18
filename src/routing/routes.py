from fastapi import APIRouter

from routing.auth import router as auth
from routing.general_stats import router as general_stats
from routing.games import router as games


router = APIRouter()


def get_apps_router():
    router.include_router(auth)
    router.include_router(general_stats)
    router.include_router(games)
    return router
