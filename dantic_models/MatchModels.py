from .BaseModels import BaseMatch, BaseUser


class MatchFullModel(BaseMatch):
    users: list[BaseUser]
