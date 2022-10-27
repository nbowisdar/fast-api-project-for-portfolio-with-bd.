from fastapi import HTTPException
from fastapi import status
from pydantic import EmailStr
from fastapi.responses import RedirectResponse
from schemas.base_models import BaseUser
from schemas.user_models import UserUpdatePass, UserFullModel, UserResetPass
from src.utils.security.jwt.jwt_token import is_authenticated
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
        query.update_password(user.email, user.old_password, user.new_password)
        logger.info(f'{user.email} - password update')
        return {f'{user.email} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )

# TODO finish it
@users_router.put('/reset_password')
def reset_password(email: EmailStr | None = None, auth2=Depends(is_authenticated),
                   data: UserResetPass | None = None):
    if email:
        if is_email_in_db(email):
            send_code(email)
            return {'check your email, you will bet a reset link'}

    if auth2 and data:
        query.reset_password(data.email, data.new_password)



