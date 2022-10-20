from peewee import *
from baseModels import ShowUser
from playhouse.shortcuts import model_to_dict
import logging
logging.basicConfig(level=logging.INFO)
db = PostgresqlDatabase('game',
                        host='localhost',
                        port=5432,
                        user='test_user',
                        password='root')


class MyUser(Model):
    name = CharField(unique=True)
    password = CharField()
    balance = IntegerField()

    class Meta:
        database = db


def show_all() -> ShowUser:
    user = MyUser.select().where(MyUser.name == 'vova').get()
    return ShowUser(**model_to_dict(user))


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


def update_balance(name: str, value: int):
    try:
        user = MyUser.get(name=name)
        user.balance = value
        user.save()
        logging.info(f'{name} - balance updated, new value: {value}')

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

