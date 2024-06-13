from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy import select

from core.config.database import db_helper
from models.base import User, Role
from schemas.game import GameSearchSchema
from services.game import game_searcher, game_downloader
from users.dependencies import get_current_active_user, get_current_superuser

router = APIRouter()


@router.get("/game/search", tags=["game search"], response_model=GameSearchSchema)
async def game_search(game_name: str, user: User = Depends(get_current_active_user)):
    """
    Осуществляет поиск настольных игр по имени game_name

    Возвращает GameSearchSchema объект
    """
    return await game_searcher.search_game(game_name=game_name)


@router.get("/game/max_bgg", tags=["for debugging"])
async def game_max_bgg(user: User = Depends(get_current_superuser)):
    return await game_downloader.get_max_bgg()


@router.post("/games", tags=["for debugging"], status_code=status.HTTP_200_OK)
async def download_games(
    start: int,
    end: int,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_superuser),  # add only admin
):
    """
    Подгружает игры с bgg. Если не указывать start, то берется максимлаьное значение bgg_id из БД
    """
    background_tasks.add_task(game_downloader.download_games, start=start, end=end)
    max_bgg_id = await game_downloader.get_max_bgg()
    return {"message": "Задача по загрузке игр запущена.", "max_bgg_id": max_bgg_id}


@router.get("/db", tags=["for debugging"])
async def test_db(user: User = Depends(get_current_superuser)):
    async with db_helper.get_db_session_context() as session:
        stmt = select(Role)
        row = await session.execute(stmt)
        return row.scalars().all()
