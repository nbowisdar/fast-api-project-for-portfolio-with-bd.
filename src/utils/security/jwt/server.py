# from fastapi import Depends, APIRouter
# from jose import jwt, JWTError
# from fastapi.security import OAuth2PasswordBearer
# from .jwt_token import create_access_token, jwt_router
# from schemas.base_models import ServerKey
# from schemas.base_models import Token
# from schemas.token_models import TokenWithType
# from datetime import timedelta
# from src.utils.tools.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# from ...errors.auth_errors import credentials_exception
# from loguru import logger
# from .jwt_token import oauth2_scheme
#
#
# #oauth2_scheme_for_server = OAuth2PasswordBearer(tokenUrl="authenticate_server")
# KEY = '123'
#
# server_jwt_router = APIRouter()
#
# # @server_jwt_router.post("/authenticate_server", response_model=TokenWithType)
# # def authenticate_server(key: ServerKey):
# #     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     jwt_token = create_access_token({'server_key': key.secret_key}, access_token_expires)
# #     return {
# #         'access_token': jwt_token,
# #         'token_type': 'server'
# #     }
#
#
# @server_jwt_router.get('/test_access_from_server')
# def test_access_from_server(token: str = Depends(oauth2_scheme)):
#     logger.info(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
#     logger.info('test')
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         server_key: str = payload.get("token_type")
#         if server_key is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     return {'authenticate': 'true'}
#
