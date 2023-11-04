from .add_nft_uris import add_nft_uris
from .add_soulbound_uris import add_soulbound_uris
from brownie import CommunityVault, NFTGifts, SoulboundBadges, Users, accounts, config, network

dev_wallet = accounts.add(config["wallets"]["from_key_1"])

CONSOLE_SEPARATOR = "--------------------------------------------------------------------------"


def get_account_from_pk(index: int) -> object:
    return accounts.add(config["wallets"][f"from_key_{index}"])


def main():
    # NETWORK
    print(CONSOLE_SEPARATOR)
    print("CURRENT NETWORK: ", network.show_active())
    print(CONSOLE_SEPARATOR)
    dev_wallet = get_account_from_pk(1)
    print(f"WALLET USED FOR DEPLOYMENT: {dev_wallet.address}")
    verify_flag = config["networks"][network.show_active()]["verify"]

    # SETUP
    asset = config["networks"][network.show_active()]["deposit_asset"]
    vault_name = "Real Fans Community Pool"
    vault_symbol = "RFCP"

    print(CONSOLE_SEPARATOR)
    print("SOULBOUND BADGES DEPLOYMENT:")
    soulbound_badges = SoulboundBadges.deploy({"from": dev_wallet}, publish_source=verify_flag)
    print()

    print(CONSOLE_SEPARATOR)
    print("USERS DB DEPLOYMENT:")
    users = Users.deploy({"from": dev_wallet}, publish_source=verify_flag)
    print()

    print(CONSOLE_SEPARATOR)
    print("COMMUNITY VAULT DEPLOYMENT:")
    vault = CommunityVault.deploy(asset, vault_name, vault_symbol, {"from": dev_wallet}, publish_source=verify_flag)
    print()

    print(CONSOLE_SEPARATOR)
    print("NFT GIFTS DEPLOYMENT:")
    nft_gifts = NFTGifts.deploy(vault.address, users.address, {"from": dev_wallet}, publish_source=verify_flag)
    print()

    print(CONSOLE_SEPARATOR)
    print("SOULBOUND URIS SETUP:")
    add_soulbound_uris(dev_wallet, soulbound_badges.address)
    print()

    print(CONSOLE_SEPARATOR)
    print("NFT URIS SETUP:")
    add_nft_uris(dev_wallet, nft_gifts.address)
    print()
