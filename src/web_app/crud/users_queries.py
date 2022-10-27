from schemas.token_models import DecodedToken
from schemas.user_models import BaseUser, UserPlural, UserFullModel
from playhouse.shortcuts import model_to_dict
from src.web_app.models.tables import *
from loguru import logger
from src.utils.security.paswords_val import Password
from src.utils.database.connect_to_db import db
from src.utils.security.jwt.jwt_token import create_access_token, encrypt_token, oauth2_scheme
from fastapi import Depends


def create_user(mail: str, login: str, password: str) -> str:
    p = Password(password, validate=True)
    with db.atomic():
        User.create(email=mail, login=login, password=p.hash_password)
    logger.info('User created')
    return login


def login(login: str, password: str) -> str:
    with db.atomic():
        user = User.get_or_none(login=login)
        if not user:
            # raise ValueError('wrong credentials')
            raise ValueError('wrong login')
        # check password
        p = Password(password)
        true_password = user.password
        if not p.check_password(true_password):
            raise ValueError('wrong password')

        data = {"sub": login,
                'position': 'user'}
        token = create_access_token(data)
        return token


def get_user(user: dict = Depends(encrypt_token)) -> UserFullModel:
    dec_token = DecodedToken(**user)
    with db.atomic():
        user = User.get(login=dec_token.login)
        return UserFullModel(
            id=user.id,
            email=user.email,
            login=user.login,
            password=user.password,
            balance=user.balance,
            best_score=user.best_score,
            created_date=user.created_date,
        )


def update_password(login: str, old_password: str, new_password: str):
    with db.atomic():
        user = User.get(login=login)
        p_old = Password(old_password, validate=True)
        if not p_old.check_password(user.password):
            raise ValueError('wrong password')
        p_new = Password(new_password, validate=True)
        user.password = p_new.hash_password
        user.save()
    logger.info(f'{login} - password updated')


def reset_password(login: str, new_password: str):
    with db.atomic():
        user = User.get(email=login)
        p = Password(new_password, validate=True)
        user.password = p.hash_password
        user.save()
    logger.info(f'{login} - password updated')


def get_login_by_email(email: str) -> str:
    with db.atomic():
        user = User.get_or_none(email=email)
        if user:
            return user.email
    raise ValueError('wrong email')


def is_new_email(email: str) -> bool:
    with db.atomic():
        user = User.get_or_none(email=email)
        if not user:
            return True
        raise ValueError('this email is already exists')


if __name__ == '__main__':
    with db.atomic():
        user = User.get_or_none(email='test@mailg.ro')
        print(user)
