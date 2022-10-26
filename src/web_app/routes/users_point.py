from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.base_models import BaseUser
from schemas.user_models import UserUpdatePass, UserFullModel
from src.web_app.crud import users_queries as db
from loguru import logger
from fastapi import APIRouter, Depends
from src.web_app.crud.users_queries import get_user

users_router = APIRouter()


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


@users_router.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = db.login(form_data.username, form_data.password)
        return {'login': 'success',
                "access_token": token}
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
        db.update_password(user.login, user.old_password, user.new_password)
        logger.info(f'{user.login} - password update')
        return {f'{user.login} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )