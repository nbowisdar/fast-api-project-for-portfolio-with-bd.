from peewee import *
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()
db = PostgresqlDatabase(database=os.getenv('DB_NAME'),
                        host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'))


class NFT(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


class MyUser(Model):
    email = CharField(unique=True)
    login = CharField(unique=True)
    password = CharField()
    balance = FloatField(default=0)
    best_score = IntegerField(default=0)
    created_date = DateField(default=datetime.now().strftime("%Y-%m-%d"))

    class Meta:
        database = db


class UserNFT(Model):
    user = ForeignKeyField(MyUser, backref='nfts')
    NFT = ForeignKeyField(NFT, backref='users_with_nft')

    class Meta:
        database = db


class Match(Model):
    price_enter = FloatField()
    number_participants = IntegerField(null=True)
    money_for_winner = FloatField()
    winner = ForeignKeyField(MyUser)
    ended = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        database = db


class UserMatch(Model):
    user = ForeignKeyField(MyUser, backref='matches')
    match = ForeignKeyField(Match, backref='participants')

    class Meta:
        database = db


db.create_tables([NFT, MyUser, UserNFT, Match, UserMatch])