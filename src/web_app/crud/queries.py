from schemas.user_models import BaseUser, AllUsers
from playhouse.shortcuts import model_to_dict
from src.web_app.models.tables import *
from loguru import logger
from src.utils.paswords_val import Password
from src.utils.database.connect_to_db import db


def show_all_users() -> AllUsers:
    rez = {'users': []}
    users = MyUser.select()
    for user in users:
        rez['users'].append(BaseUser(**model_to_dict(user)))
    return AllUsers(**rez)


def create_user(mail: str, login: str, password: str) -> str:
    p = Password(password)
    with db.atomic():
        MyUser.create(email=mail, login=login, password=p.hash_password())
    logger.info('User created')
    return login


def drop_user(login) -> str:
    with db.atomic():
        user = MyUser.get(login=login)
        user.delete_instance()
    return login


def update_balance(login: str, tokens: int):
    with db.atomic():
        user = MyUser.get(login=login)
        user.balance = tokens
        user.save()
    logger.info(f'{login} - balance updated, new value: {tokens}')


def reset_password(login: str, new_password: str):
    with db.atomic():
        user = MyUser.get(login=login)
        p = Password(new_password)
        user.password = p.hash_password()
        user.save()
    logger.info(f'{login} - password updated')


def update_password(login: str, old_password: str, new_password: str):
    with db.atomic():
        user = MyUser.get(login=login)
        p_old = Password(old_password)
        if p_old.hash_password() != user.password:
            raise ValueError('wrong password')
        p_new = Password(new_password)
        user.password = p_new.hash_password()
        user.save()
    logger.info(f'{login} - password updated')


#########
'queries Match'


def create_match(price: float, number_participants: int, user_id: int):
    money = price * number_participants
    with db.atomic():
        match = Match.create(price_enter=price, number_participants=number_participants,
                             money_for_winner=money, winner=user_id)
        match.save()
    logger.info('match created')
    return match.get_id()


#create_match(20, 4, 1)
