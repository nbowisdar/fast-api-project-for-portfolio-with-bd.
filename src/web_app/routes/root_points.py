from fastapi import HTTPException, Depends, Query
from fastapi import status
from schemas.user_models import UserResetPass
from src.utils.errors.auth_errors import credentials_exception, only_root_exception
from src.utils.security.jwt.jwt_token import is_root
from src.web_app.crud import root_queires as query
from loguru import logger
from fastapi import APIRouter
from src.web_app.crud import matches_queries as match

root_router = APIRouter(prefix='/root')


@root_router.get("/show_all_users",)
async def show_all_users(root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    data = query.show_all_users()
    return {data.json()}


# TODO maybe this can be users point
@root_router.put('/reset_password')
def reset_password(user: UserResetPass):
    try:
        query.reset_password(user.login, user.new_password)
        logger.info(f'{user.login} - password update')
        return {f'{user.login} - password update'}

    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )

@root_router.put('/update_balance')
def update_balance(username: str, new_bal: float,
                   root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    try:
        query.update_balance(username, new_bal)
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(err)
        )

############
'match'
############


@root_router.post('/start_new_match')
def start_new_match(price: float, participants: str = Query(description='user_id separated by space', example='1 2 3...'),
                    root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    try:
        match_id = match.match_started(price, participants)
        return {f'Match №{match_id} - started'}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_408_CONFLICT,
            detail=str(err)
        )


@root_router.post('/finish_match')
def finish_match(match_id: int, winner_id: int,
                 root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    try:
        match.match_ended(match_id, winner_id)
        logger.info(f'Match №{match_id} finished')
        return {f'Match №{match_id} - finished'}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_408_CONFLICT,
            detail=str(err)
        )




# @root_router.delete('/drop_user')
# async def drop_user(login: str):
#     try:
#         query.drop_user(login)
#         return {f'{login} - deleted'}
#     except Exception as err:
#         logger.error(err)
#         return {err}