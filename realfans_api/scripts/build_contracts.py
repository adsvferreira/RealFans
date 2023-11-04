from brownie import (
    config,
    project,
    network,
)

import yaml


def build_contracts(net: str) -> dict:

    my_project = project.load(".")
    my_project.load_config()
    network.connect(net)
    NETWORK_PATH = config["networks"][net]

    return {"users": my_project.Users.at(NETWORK_PATH["users_address"]),
            "nft": my_project.NFTGifts.at(NETWORK_PATH["nft_gifts_address"]),
            "soulbound": my_project.SoulboundBadges.at(NETWORK_PATH["soulbound_address"]),
            "vault": my_project.CommunityVault.at(NETWORK_PATH["community_vault_address"]),
            }