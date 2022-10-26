from .config import *
from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    login: str
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class BaseMatch(BaseModel):
    price_enter: float
    money_for_winner: float
    winner_id: int
    ended: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class BaseNft(BaseModel):
    name: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ServerKey(BaseModel):
    secret_key: str


class Token(BaseModel):
    access_token: str


class Root(BaseModel):
    username: str
    password: str
