from brownie import (
    config,
    Users,
    NFTGifts,
    CommunityVault,
    SoulboundBadges,
) 


def build_contracts(network: str) -> dict:
    NETWORK_PATH = config["networks"][network]
    return {"users": Users.at(NETWORK_PATH["users_address"]),
            "nft": NFTGifts.at(NETWORK_PATH["nft_gifts_address"]),
            "soulbound": SoulboundBadges.at(NETWORK_PATH["soulbound_address"]),
            "vault": CommunityVault.at(NETWORK_PATH["community_vault_address"]),
            }