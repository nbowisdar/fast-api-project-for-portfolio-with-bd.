from typing import Any, List
from pydantic.utils import GetterDict
from pydantic import BaseModel
from peewee import ModelSelect


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res


class BaseUser(BaseModel):
    name: str
    balance: float

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ShowUser(BaseUser):
    id: int


class CreateUser(BaseUser):
    password: str


class AllUsers(BaseModel):
    users: list[BaseUser]
