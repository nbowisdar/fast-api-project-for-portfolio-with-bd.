from fastapi import HTTPException
from fastapi import status
from schemas.base_models import BaseUser
from src.web_app.crud import queries as db
from loguru import logger
from server import app


@app.post('/create_user')
async def create_user(user: BaseUser):
    try:
        db.create_user(user.email, user.login, user.password)
        logger.info(f'{user.login} - created')
        return {f'{user.login} - created'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@app.delete('/drop_user')
async def drop_user(login: str):
    try:
        db.drop_user(login)
        return {f'{login} - deleted'}
    except Exception as err:
        logger.error(err)
        return {err}


@app.put('/update_balance')
def update_balance(login: str, tokens: int):
    try:
        db.update_balance(login, tokens)
        logger.info(f'{login} - balance update')
        return {f'{login} - balance update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@app.put('/reset_password')
def reset_password(login: str, new_password: str):
    try:
        db.reset_password(login, new_password)
        logger.info(f'{login} - password update')
        return {f'{login} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@app.put('/update_password')
def update_password(login: str, old_password: str, new_password: str):
    try:
        db.update_password(login, old_password, new_password)
        logger.info(f'{login} - password update')
        return {f'{login} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


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
