from metadata.nft_uris import NFT_URIS
from brownie import config, network, accounts, NFTGifts


def add_nft_uris(dev_wallet, nft_gifts_address):
    nft = NFTGifts.at(nft_gifts_address)

    for uri in NFT_URIS.values():
        nft.addNewGiftURI(uri["uri"], uri["eth_value"], {"from": dev_wallet})

    print("Added all NFT URIs.")
