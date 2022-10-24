from schemas.user_models import BaseUser, UserPlural
from playhouse.shortcuts import model_to_dict
from src.web_app.models.tables import *
from loguru import logger
from src.utils.paswords_val import Password
from src.utils.database.connect_to_db import db


def show_all_users() -> UserPlural:
    rez = {'users': []}
    users = User.select()
    for user in users:
        rez['users'].append(BaseUser(**model_to_dict(user)))
    return UserPlural(**rez)


def create_user(mail: str, login: str, password: str) -> str:
    p = Password(password)
    with db.atomic():
        User.create(email=mail, login=login, password=p.hash_password())
    logger.info('User created')
    return login


def drop_user(login) -> str:
    with db.atomic():
        user = User.get(login=login)
        user.delete_instance()
    return login


def update_balance(login: str, tokens: int):
    with db.atomic():
        user = User.get(login=login)
        user.balance = tokens
        user.save()
    logger.info(f'{login} - balance updated, new value: {tokens}')


def reset_password(login: str, new_password: str):
    with db.atomic():
        user = User.get(login=login)
        p = Password(new_password)
        user.password = p.hash_password()
        user.save()
    logger.info(f'{login} - password updated')


def update_password(login: str, old_password: str, new_password: str):
    with db.atomic():
        user = User.get(login=login)
        p_old = Password(old_password)
        if p_old.hash_password() != user.password:
            raise ValueError('wrong password')
        p_new = Password(new_password)
        user.password = p_new.hash_password()
        user.save()
    logger.info(f'{login} - password updated')


#########
'queries Match'


def match_started(price: float, users: list[int]):
    money = price * len(users)
    with db.atomic():
        match = Match.create(price_enter=price, money_for_winner=money)
    with db.atomic():
        #create query in format:
        # [(match_id, user_id-1), (match_id, user_id-2)...]
        query = [(user_id, match.id) for user_id in users]
        UserMatch.insert_many(query, fields=[UserMatch.user, UserMatch.match]).execute()
    logger.info(f'Match {match.get_id()} started')
    #return match.get_id()


def match_ended(match_id: int, winner_id: int):
    with db.atomic():
        match = Match.get(id=match_id)
        match.winner = winner_id
        match.ended = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        match.finished = True
        match.save()
    logger.info(f'Match №{match_id} ended')


#match_started(5, [1,2,3])
#match_ended(4, 2)