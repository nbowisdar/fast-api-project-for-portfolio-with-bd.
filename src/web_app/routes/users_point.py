from fastapi import HTTPException, status
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


users_router = APIRouter(prefix='/user')


@users_router.post('/signup')
async def sign_up(user: BaseUser):
    try:
        # if email exists raise an error
        query.is_new_email(user.email)
        Password.validation_email(user.email)
        Password.validation_password(user.password)
        data = {
            "user_data": user.json(),
            "type": "register"
        }
        # creating token with credential, and send it on users email
        token = create_access_token(data, timedelta(minutes=30))
        # send message formate url + token
        await send_register_link(recv_mail=user.email, end_point='/user/create_acc/', token=token)
        return {f'check your email'}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )


@users_router.get('/create_acc/{token}')
async def create_user(token: str):
    # when user open link from email we unpack his credential
    # and create a new account
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
async def show_profile(user: UserFullModel = Depends(get_user)):
    return {user.json()}


@users_router.put('/update_password')
async def update_password(old_password: str, new_password: str, user=Depends(get_user)):
    # we allow update password if user is logged in
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
async def reset_password(email: str):
    # we need users login because it will help reset his password later
    # the line below will throw an error if email is wrong.
    # otherwise - return users login
    login = query.get_login_by_email(email=email)

    # we create special JWT token and put it inside this link.
    data = {"sub": login,
            'position': 'user'}
    token = create_access_token(data, expires_delta=timedelta(minutes=3))
    # we send link to users email.
    # when user opens this link - we take back JWT
    # and allow them to change password

    await send_link(recv_mail=email, token=token, end_point='/user/set_password/')
    return {'check your email, you will bet a reset link'}


@users_router.get('/set_password/{token}')
async def set_password(token: str, new_password: str | None = None):
    # user should have token that we send them on email
    if not token:
        raise HTTPException(403, {'response': 'forbidden'})
    try:
        login = get_login_from_token(token)
        if not new_password:
            return {'response': 'please send new password'}
        query.reset_password(login, new_password)
        return {'response': "Congrats! You've just set new password!"}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )