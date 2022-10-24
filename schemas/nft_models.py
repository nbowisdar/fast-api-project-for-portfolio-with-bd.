from .base_models import BaseNft, BaseUser


class NftFullModel(BaseNft):
    users_why_has_this_nft: list[BaseUser]
