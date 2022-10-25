from peewee import Model, CharField
from src.utils.database.connect_to_db import db


class Admin(Model):
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

if __name__ == '__main__':
    with db.atomic():
        db.create_tables([Admin])