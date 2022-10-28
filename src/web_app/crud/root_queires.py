from schemas.user_models import BaseUser, UserPlural
from playhouse.shortcuts import model_to_dict
from src.utils.security.jwt.jwt_token import create_access_token
from src.web_app.models.tables import *
from loguru import logger
from src.utils.database.connect_to_db import db
from src.utils.tools.config import ROOT_PASSWORD, ROOT_USERNAME


def login(login: str, password: str) -> str:
    if ROOT_USERNAME == login and ROOT_PASSWORD == password:
        data = {"sub": login,
                'position': 'root'}
        token = create_access_token(data)
        return token
    raise ValueError('wrong credentials')


def show_all_users() -> UserPlural:
    rez = {'users': []}
    users = User.select()
    for user in users:
        rez['users'].append(BaseUser(**model_to_dict(user)))
    return UserPlural(**rez)


def update_balance(login: str, new_bal: float):
    with db.atomic():
        user = User.get(login=login)
        user.balance = new_bal
        user.save()
    logger.info(f'{login} - balance updated, new value: {new_bal}')


# def drop_user(login) -> str:
#     with db.atomic():
#         user = User.get(login=login)
#         user.delete_instance()
#     return login