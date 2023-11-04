from metadata.soulbound_uris import SOULBOUND_URIS
from brownie import config, network, accounts, SoulboundBadges


def add_soulbound_uris(dev_wallet, soulbound_address):
    soulbound_contract = SoulboundBadges.at(soulbound_address)

    for uri in SOULBOUND_URIS.values():
        soulbound_contract.addNewBadgeURI(uri, {"from": dev_wallet})

    print("Added all Soulbound URIs.")
