from fastapi import HTTPException
from fastapi import status
from schemas.base_models import BaseUser
from src.web_app.crud import matches_queries as db
from loguru import logger
from src.web_app.server import app


@app.post('/start_new_match')
def start_new_match(price: float, participants: list[int], ):
    try:
        match_id = db.match_started(price, participants)
        logger.info(f'Match №{match_id} started')
        return {f'Match №{match_id} - started'}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_408_CONFLICT,
            detail=str(err)
        )


@app.post('/finish_match')
def finish_match(match_id: int, winner_id: int):
    try:
        match_id = db.match_ended(match_id, winner_id)
        logger.info(f'Match №{match_id} finished')
        return {f'Match №{match_id} - finished'}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_408_CONFLICT,
            detail=str(err)
        )
