from fastapi import HTTPException
from fastapi import status
from schemas.base_models import BaseUser
from src.web_app.crud import users_queries as db
from loguru import logger
from fastapi import APIRouter

users_router = APIRouter()


@users_router.get("/show_all_users")
async def show_all_users():
    data = db.show_all_users()
    return {data.json()}


@users_router.post('/create_user')
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


@users_router.delete('/drop_user')
async def drop_user(login: str):
    try:
        db.drop_user(login)
        return {f'{login} - deleted'}
    except Exception as err:
        logger.error(err)
        return {err}


@users_router.put('/update_balance')
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


@users_router.put('/reset_password')
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


@users_router.put('/update_password')
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