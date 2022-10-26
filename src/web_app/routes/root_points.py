from fastapi import HTTPException
from fastapi import status
from schemas.base_models import BaseUser
from schemas.user_models import LoginModel, UserResetPass, UserUpdatePass
from src.web_app.crud import users_queries as db
from loguru import logger
from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/show_all_users")
async def show_all_users():
    data = db.show_all_users()
    return {data.json()}



@root_router.delete('/drop_user')
async def drop_user(login: str):
    try:
        db.drop_user(login)
        return {f'{login} - deleted'}
    except Exception as err:
        logger.error(err)
        return {err}


@root_router.put('/update_balance')
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


@root_router.put('/reset_password')
def reset_password(user: UserResetPass):
    try:
        db.reset_password(user.login, user.new_password)
        logger.info(f'{user.login} - password update')
        return {f'{user.login} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )

