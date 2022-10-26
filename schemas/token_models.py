from .base_models import Token
from pydantic import BaseModel


class TokenWithType(Token):
    token_type: str


class DecodedToken(BaseModel):
    login: str | None
    position: str | None
