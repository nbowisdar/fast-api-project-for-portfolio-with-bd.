from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.base_models import BaseUser
from schemas.user_models import UserUpdatePass, UserFullModel
from src.web_app.crud import users_queries as query
from loguru import logger
from fastapi import APIRouter, Depends
from src.web_app.crud.users_queries import get_user

users_router = APIRouter(prefix='/user')


@users_router.post('/signup')
async def create_user(user: BaseUser):
    try:
        query.create_user(user.email, user.login, user.password)
        logger.info(f'{user.login} - created')
        return {f'{user.login} - created'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@users_router.get('/profile')
def show_profile(user: UserFullModel = Depends(get_user)):
    return {user.json()}


@users_router.put('/update_password')
def update_password(user: UserUpdatePass):
    try:
        query.update_password(user.login, user.old_password, user.new_password)
        logger.info(f'{user.login} - password update')
        return {f'{user.login} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


