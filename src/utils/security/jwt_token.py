from pydantic import BaseModel
from schemas.config import PeeweeGetterDict
from src.utils.tools.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.utils.security.paswords_val import Password
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends, status, APIRouter
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.utils.database.connect_to_db import db
from src.web_app.models.admin_model import Admin
from playhouse.shortcuts import model_to_dict


jwt_router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password, true_password):
    p = Password(password)
    return p.check_password(true_password)


def authenticate_user(username: str, password: str) -> Admin:
    user = Admin.get_or_none(username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@jwt_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@jwt_router.get('/check_authentication')
async def test(token: str = Depends(oauth2_scheme)):
    return {'authentication': 'true'}


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = Admin.get_or_none(username=username)
#     if user is None:
#         raise credentials_exception
#     return user