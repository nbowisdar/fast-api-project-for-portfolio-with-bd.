from fastapi import HTTPException
from fastapi import status
from schemas.base_models import BaseUser
from schemas.user_models import UserFullModel
from src.utils.email.run import send_link, send_register_link
from src.utils.security.jwt.jwt_token import get_login_from_token, create_access_token, decode_register_token
from src.utils.security.paswords_val import Password
from src.web_app.crud import users_queries as query
from loguru import logger
from fastapi import APIRouter, Depends
from src.web_app.crud.users_queries import get_user
from datetime import timedelta
from fastapi.responses import RedirectResponse

users_router = APIRouter(prefix='/user')


@users_router.post('/signup')
async def create_user(user: BaseUser):
    try:
        query.is_new_email(user.email)
        Password.validation_email(user.email)
        Password.validation_password(user.password)

        data = {
            "user_data": user.json(),
            "type": "register"
        }
        token = create_access_token(data, timedelta(minutes=30))
        send_register_link(recv_mail=user.email, end_point='/user/create_acc/', token=token)
        return {f'check your email'}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )



@users_router.get('/create_acc/{token}')
async def create_user(token: str):
    user = decode_register_token(token)
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


@users_router.put('/update_password', )
def update_password(old_password: str, new_password: str, user=Depends(get_user)):
    try:
        query.update_password(user.login, old_password, new_password)
        logger.info(f'{user.email} - password update')
        return {f'{user.email} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@users_router.put('/reset_password/send_link')
def reset_password(email: str):
    login = query.get_login_by_email(email=email)
    send_link(recv_mail=email, login=login, end_point='/user/check_mail/')
    return {'check your email, you will bet a reset link'}


@users_router.get('/check_mail/{token}')
def check_email(token: str):
    try:
        login = get_login_from_token(token)
        return RedirectResponse(f'/user/set_password?login={login}')
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@users_router.get('/set_password')
def set_password(login: str, new_password: str | None = None):
    if not new_password:
        return {'please send new password'}
    try:
        query.reset_password(login, new_password)
        return {"Congrats! You've just set new password!"}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )