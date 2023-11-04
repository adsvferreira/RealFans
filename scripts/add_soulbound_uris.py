from metadata.soulbound_uris import SOULBOUND_URIS
from brownie import config, network, accounts, SoulboundBadges


def add_soulbound_uris(dev_wallet):
    SOULBOUND_CONTRACT = config["networks"][network.show_active()]["soulbound_address"]

    soulbound_contract = SoulboundBadges.at(SOULBOUND_CONTRACT)

    for uri in SOULBOUND_URIS.values():
        soulbound_contract.addNewBadgeURI(uri, {"from": dev_wallet})

    print("Added all Soulbound URIs.")