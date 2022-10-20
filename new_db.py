from peewee import *
from baseModels import ShowUser, AllUsers
from playhouse.shortcuts import model_to_dict
import logging
from dotenv import load_dotenv
import os
logging.basicConfig(level=logging.INFO)
load_dotenv()
db = PostgresqlDatabase('game',
                        host='localhost',
                        port=5432,
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'))


class MyUser(Model):
    name = CharField(unique=True)
    password = CharField()
    balance = IntegerField()

    class Meta:
        database = db


def show_all() -> AllUsers:
    rez = {'users': []}
    user = MyUser.select()
    for user in user:
        rez['users'].append(ShowUser(**model_to_dict(user)))
    return AllUsers(**rez)


def create_user(name: str, password: str, balance = 0) -> str | None:
    try:
        MyUser.create(name=name, password=password, balance=balance)
        logging.info('User created')
        return name

    except Exception as err:
        logging.error(err)


def drop_user(name) -> str | None:
    try:
        user = MyUser.get(name=name)
        user.delete_instance()
        return name

    except Exception as err:
        logging.error(err)


def update_balance(name: str, tokens: int):
    try:
        user = MyUser.get(name=name)
        user.balance = tokens
        user.save()
        logging.info(f'{name} - balance updated, new value: {tokens}')

    except Exception as err:
        logging.error(err)


def update_password(name: str, new_password: str):
    try:
        user = MyUser.get(name=name)
        user.password = new_password
        user.save()
        logging.info(f'{name} - password updated')

    except Exception as err:
        logging.error(err)