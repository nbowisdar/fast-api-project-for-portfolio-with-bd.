from loguru import logger
from src.utils.tools.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
    logger.info(token)
    print(token)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = {
        'login': payload.get('sub'),
        'position': payload.get('position')
    }
    return data
