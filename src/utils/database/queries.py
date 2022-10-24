# import sys
# sys.path.append("../../..")
# from game_back.dantic_models.UserModels import BaseUser, AllUsers
from schemas.user_models import BaseUser, AllUsers
from playhouse.shortcuts import model_to_dict
from game_back.src.utils.database.tables import *


def show_all_users() -> AllUsers:
    rez = {'users': []}
    users = MyUser.select()
    for user in users:
        rez['users'].append(BaseUser(**model_to_dict(user)))
    return AllUsers(**rez)


def create_user(mail: str, login: str, password: str) -> str:
    MyUser.create(email=mail, login=login, password=password)
    logging.info('User created')
    return login


def drop_user(login) -> str:
    user = MyUser.get(login=login)
    user.delete_instance()
    return login


def update_balance(login: str, tokens: int):
    user = MyUser.get(login=login)
    user.balance = tokens
    user.save()
    logging.info(f'{login} - balance updated, new value: {tokens}')


def reset_password(login: str, new_password: str):
    user = MyUser.get(login=login)
    user.password = new_password
    user.save()
    logging.info(f'{login} - password updated')


def update_password(login: str, old_password: str, new_password: str):
    user = MyUser.get(login=login)
    if old_password != user.password:
        raise ValueError('wrong password')
    user.password = new_password
    user.save()
    logging.info(f'{login} - password updated')


#########
'queries Match'

def create_match(price: float, number_participants: int, user_id: int):
    money = price*number_participants
    match = Match.create(price_enter=price, number_participants=number_participants,
                         money_for_winner=money, winner=user_id)
    match.save()
    logging.info('match created')
    return match.get_id()


create_match(20, 4, 1)