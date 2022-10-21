from peewee import *
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
logging.basicConfig(level=logging.INFO)

load_dotenv()
db = PostgresqlDatabase('game',
                        host='localhost',
                        port=5432,
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'))


class NFT(Model):
    name = CharField(unique=True)


class MyUser(Model):
    email = CharField(unique=True)
    login = CharField(unique=True)
    password = CharField()
    balance = IntegerField()
    best_score = IntegerField(null=True)
    created_date = DateField(default=datetime.now().strftime("%Y-%m-%d"))
    #current_nft = ForeignKeyField(NFT, null=True)

    class Meta:
        database = db


class UserNFT(Model):
    user_id = ForeignKeyField(MyUser, backref='nfts')
    NFT_id = ForeignKeyField(NFT, backref='users_with_nft')


class Match(Model):
    price_enter = FloatField()
    money_for_winner = FloatField()
    winner = ForeignKeyField(MyUser, backref='winning')
    ended = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #TODO: add nft wich each user used ?


class UserMatch(Model):
    user_id = ForeignKeyField(MyUser, backref='matches')
    match_id = ForeignKeyField(Match, backref='participants')
