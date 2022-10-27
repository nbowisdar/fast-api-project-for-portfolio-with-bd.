from .base_models import BaseUser, BaseMatch, BaseNft
from pydantic import BaseModel, EmailStr
from datetime import date


class UserFullModel(BaseUser):
    id: int
    balance: float
    best_score: int
    created_date: date = None

    matches = list[BaseMatch]
    have_nft = list[BaseNft]


class UserPlural(BaseModel):
    users: list[BaseUser]


class LoginModel(BaseModel):
    login: str
    password: str


class UserResetPass(BaseModel):
    email: EmailStr
    new_password: str


class UserUpdatePass(UserResetPass):
    old_password: str
