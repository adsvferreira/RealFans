from brownie import (
    config,
    project,
    network,
) 


def build_contracts(net: str) -> dict:
    NETWORK_PATH = config["networks"][net]
    return {"users": Users.at(NETWORK_PATH["users_address"]),
            "nft": NFTGifts.at(NEWORK_PATH["nft_gifts_address"]),
            "soulbound": SoulboundBadges.at(NETWORK_PATH["soulbound_address"]),
            "vault": CommunityVault.at(NETWORK_PATH["community_vault_address"]),
            }