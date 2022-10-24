from .base_models import BaseUser, BaseMatch, BaseNft
from pydantic import BaseModel


#class CreateUserModel(BaseUser):

class UserFullModel(BaseUser):
    id: int
    balance: float
    best_score: int
    created_date: str

    matches = list[BaseMatch]
    have_nft = list[BaseNft]



class UserPlural(BaseModel):
    users: list[BaseUser]
