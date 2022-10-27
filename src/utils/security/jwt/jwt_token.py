import json
from loguru import logger
from schemas.base_models import BaseUser
from src.utils.errors.auth_errors import credentials_exception
from src.utils.tools.config import SECRET_KEY, ALGORITHM, ROOT_USERNAME
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# return login and position in dict
def encrypt_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as err:
        logger.error(err)
        raise credentials_exception
    data = {
        'login': payload.get('sub'),
        'position': payload.get('position')
    }
    return data


def is_root(token: str = Depends(oauth2_scheme)) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as err:
        logger.error(err)
        raise credentials_exception
    if ROOT_USERNAME == payload.get('position'):
        return True
    return False


def get_login_from_token(token: str) -> str:
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get('sub')
        except JWTError as err:
            logger.error(err)
    raise ValueError('wrong token')


def decode_register_token(token: str) -> BaseUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get('user_data')
        j_user = json.loads(user)
        return BaseUser(**j_user)
    except JWTError as err:
        logger.error(err)


