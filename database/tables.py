from peewee import *


class NFT(Model):
    name = CharField(unique=True)


class MyUser(Model):
    email = CharField(unique=True)
    login = CharField(unique=True)
    password = CharField()
    balance = IntegerField()
    best_score = IntegerField(null=True)
    created_date = DateField(default=datetime.now().strftime("%Y-%m-%d"))
    current_nft = ForeignKeyField(NFT, null=True)

    class Meta:
        database = db


class UserNFT(Model):
    user_id = ForeignKeyField(MyUser)
    NFT_id = ForeignKeyField(NFT)


class Match(Model):
    price_enter = FloatField()
    money_for_winner = FloatField()
    winner = ForeignKeyField(MyUser, backref='winning')
    ended = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class UserMatch(Model):
    user_id = ForeignKeyField(MyUser)
    match_id = ForeignKeyField(Match)
