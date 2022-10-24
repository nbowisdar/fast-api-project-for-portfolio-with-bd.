from fastapi import HTTPException
from fastapi import status
from schemas.base_models import BaseUser
from src.web_app.crud import queries as db
from loguru import logger
from src.web_app.server import app


@app.post('/create_match')
def create_match(price: float, number_participants: int, user_id: int):
    try:
        match_id = db.create_match(price, number_participants, user_id)
        logger.info(f'{match_id} - ended')
        return {f'Match №{match_id} - ended'}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_408_CONFLICT,
            detail=str(err)
        )
