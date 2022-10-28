from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from src.web_app.crud.root_queires import login as root_login
from src.web_app.crud.users_queries import login as user_login

base_router = APIRouter()


@base_router.post('/login/')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                root: bool = False,
                ):
    try:
        if root:
            token = root_login(form_data.username, form_data.password)
        else:
            token = user_login(form_data.username, form_data.password)
        if token:
            return {'login': 'success',
                    "access_token": token}
        raise Exception('wrong credential')
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )
