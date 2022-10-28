from fastapi import HTTPException, Depends, Query
from fastapi import status
from src.utils.errors.auth_errors import only_root_exception
from src.utils.security.jwt.jwt_token import is_root
from src.web_app.crud import root_queires as query
from loguru import logger
from fastapi import APIRouter
from src.web_app.crud import matches_queries as match

root_router = APIRouter(prefix='/root')


@root_router.get("/show_all_users", )
async def show_all_users(root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    data = query.show_all_users()
    return {data.json()}


@root_router.put('/update_balance')
async def update_balance(login: str, new_bal: float, root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    try:
        query.update_balance(login, new_bal)
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
async def start_new_match(price: float,
                          participants: str = Query(description='user_id separated by space', example='1 2 3...'),
                          root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    try:
        match_id = match.begin_match(price, participants)
        return {f'Match №{match_id} - started'}
    except Exception as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_408_CONFLICT,
            detail=str(err)
        )


@root_router.post('/finish_match')
async def finish_match(match_id: int, winner_id: int, root: bool = Depends(is_root)):
    if not root:
        raise only_root_exception
    try:
        match.finish_match(match_id, winner_id)
        logger.info(f'Match №{match_id} - finished')
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
