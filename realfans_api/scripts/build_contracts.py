from brownie import (
    config,
    project,
    network,
)

from realfans_api.enums import BROWNIE_PROJECT


def build_contracts(net: str) -> dict:

    my_project = BROWNIE_PROJECT
    NETWORK_PATH = config["networks"][net]

    return {"users": my_project.Users.at(NETWORK_PATH["users_address"]),
            "nft": my_project.NFTGifts.at(NETWORK_PATH["nft_gifts_address"]),
            "soulbound": my_project.SoulboundBadges.at(NETWORK_PATH["soulbound_address"]),
            "vault": my_project.CommunityVault.at(NETWORK_PATH["community_vault_address"]),
            }