from peewee import Model, CharField, ForeignKeyField, FloatField,\
    IntegerField, DateTimeField, DateField, BooleanField
from src.utils.database.connect_to_db import db
from datetime import datetime


class NFT(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


class User(Model):
    email = CharField(unique=True)
    login = CharField(unique=True)
    password = CharField()
    balance = FloatField(default=0)
    best_score = IntegerField(default=0)
    created_date = DateField(default=datetime.now().strftime("%Y-%m-%d"))

    class Meta:
        database = db
        db_table = 'user_acc'


class UserNFT(Model):
    user = ForeignKeyField(User, backref='nfts')
    NFT = ForeignKeyField(NFT, backref='users_with_nft')

    class Meta:
        database = db


class Match(Model):
    price_enter = FloatField()
    money_for_winner = FloatField()
    winner = ForeignKeyField(User, null=True)
    started = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ended = DateTimeField(null=True)
    finished = BooleanField(default=False)

    class Meta:
        database = db


class UserMatch(Model):
    user = ForeignKeyField(User, backref='matches')
    match = ForeignKeyField(Match, backref='participants')

    class Meta:
        database = db


if __name__ == '__main__':
    with db.atomic():
        db.create_tables([NFT, User, UserNFT, Match, UserMatch])
