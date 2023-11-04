from metadata.nft_uris import NFT_URIS
from brownie import config, network, accounts, NFTGifts

dev_wallet = accounts.add(config["wallets"]["from_key_1"])

NFT_CONTRACT = config["networks"][network.show_active()]["nft_gifts_address"]

nft = NFTGifts.at(NFT_CONTRACT)

for uri in NFT_URIS.values():
    nft.addNewGiftURI(uri["uri"], uri["eth_value"])

print("Added all NFT URIs.")