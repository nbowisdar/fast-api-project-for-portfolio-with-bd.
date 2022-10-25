from src.web_app.models.tables import *
from loguru import logger
from src.utils.database.connect_to_db import db


def match_started(price_enter: float, users: list[int]) -> int:
    money = price_enter * len(users)
    with db.atomic():
        match = Match.create(price_enter=price_enter, money_for_winner=money)
    with db.atomic():
        # update users' balances
        for user_id in users:
            user = User.get(id=user_id)
            user.balance -= price_enter
            user.save()
    with db.atomic():
        # create query in format:
        # [(match_id, user_id-1), (match_id, user_id-2)...]
        query = [(user_id, match.id) for user_id in users]
        UserMatch.insert_many(query, fields=[UserMatch.user, UserMatch.match]).execute()
    logger.info(f'Match {match.get_id()} has begun')
    return match.get_id()


def match_ended(match_id: int, winner_id: int) -> None:
    with db.atomic():
        match = Match.get(id=match_id)
        if match.finished:
            raise ValueError('this match is already finished!')
        match.winner = winner_id
        match.ended = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        match.finished = True
        match.save()

        # added money on winners balance
        user = User.get(id=winner_id)
        user.balance += match.money_for_winner
        user.save()
    logger.info(f'Match {match.get_id()} has finished')
