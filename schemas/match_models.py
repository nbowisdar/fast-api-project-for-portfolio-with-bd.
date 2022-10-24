from .base_models import BaseMatch, BaseUser


class MatchFullModel(BaseMatch):
    users: list[BaseUser]
