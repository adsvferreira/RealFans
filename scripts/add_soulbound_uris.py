from metadata.soulbound_uris import SOULBOUND_URIS
from brownie import config, network, accounts, SoulboundBadges

dev_wallet = accounts.add(config["wallets"]["from_key_1"])

SOULBOUND_CONTRACT = config["networks"][network.show_active()]["soulbound_address"]

soulbound_contract = SoulboundBadges.at(SOULBOUND_CONTRACT)

for uri in SOULBOUND_URIS.values():
    soulbound_contract.addNewGiftURI(uri)

print("Added all Soulbound URIs.")