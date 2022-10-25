from .base_models import BaseUser, BaseMatch, BaseNft
from pydantic import BaseModel


class UserFullModel(BaseUser):
    id: int
    balance: float
    best_score: int
    created_date: str

    matches = list[BaseMatch]
    have_nft = list[BaseNft]


class UserPlural(BaseModel):
    users: list[BaseUser]


class LoginModel(BaseModel):
    login: str
    password: str


class UserResetPass(BaseModel):
    login: str
    new_password: str


class UserUpdatePass(UserResetPass):
    old_password: str
