from peewee import Model, CharField
from src.utils.database.connect_to_db import db


class Admin(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

if __name__ == '__main__':
    with db.atomic():
        db.create_tables([Admin])
        #Admin.(username='root', password='root')
        user = Admin.get_or_none(username='root')
        if user:
            user

