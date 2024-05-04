from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy import select

from config.db.database import db_helper
from ..models.base import User, Role
from ..schemas.game import GameSearchSchema
from ..services.game import game_downloader, game_searcher
from ..utils.auth.manager import current_active_user


router = APIRouter(
    tags=['Game Search'],
)


@router.get("/game/search",
            response_model=GameSearchSchema)
async def game_search(game_name: str, user: User = Depends(current_active_user)):
    return await game_searcher.search_game(game_name=game_name)


@router.post("/games", status_code=status.HTTP_200_OK)
async def download_games(start: int, end: int, background_tasks: BackgroundTasks,
                         user: User = Depends(current_active_user)  # add only admin
                         ):
    """
    Подгружает игры с bgg. Если не указывать start, то берется максимлаьное значение bgg_id из БД
    """
    background_tasks.add_task(game_downloader.download_games, start=start, end=end)
    return {"message": "Задача по загрузке игр запущена."}


@router.get("/db")
async def test_db():
    async with db_helper.get_db_session_context() as session:
        stmt = select(Role)
        row = await session.execute(stmt)
        return row.scalars().all()
