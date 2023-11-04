from brownie import accounts, config, network
from docs.abis import erc20_abi

dev_wallet = accounts.add(config["wallets"]["from_key_1"])

URI_EXAMPLE = "https://ipfs.io/ipfs/QmfTrPkKduncJvxCybkRTsUgFk6Y3fBnQrseGGbLZR9GSZ?filename=conservative.json"
NFT_ETH_VALUE = 100_000_000_000_000  # 0.0001 weth
APPROVE_VALUE = 999_999_999_999_999_999_999_999_999_999
CREATOR_ADDR = "0xC55489B0Da14D81725509a03cF0Eb86a0a23D8eb"

asset = config["networks"][network.show_active()]["deposit_asset"]
vault_name = "Real Fans Community Pool"
vault_symbol = "RFCP"
weth = Contract.from_abi("ERC20", config["networks"][network.show_active()]["deposit_asset"], erc20_abi)

# tx1 = SoulboundBadges.deploy({"from": dev_wallet})
# soulboundBadges = SoulboundBadges[-1]
# tx2 = soulboundBadges.addNewBadgeURI(URI_EXAMPLE, NFT_ETH_VALUE, {"from": dev_wallet})
# tx3 = soulboundBadges.mintBadge(dev_wallet, URI_EXAMPLE, {"from": dev_wallet})

# soulboundBadges.getAllURIs()
# soulboundBadges.getTokenIdCounter()
# soulboundBadges.getTotalQtyOfBadge(URI_EXAMPLE)
# soulboundBadges.getBadgeQtyOf(dev_wallet, URI_EXAMPLE)

vault = CommunityVault.deploy(asset, vault_name, vault_symbol, {"from": dev_wallet})
# tx5 = weth.approve(vault.address, APPROVE_VALUE, {"from": dev_wallet})
# tx6 = vault.deposit(100_000, dev_wallet, {"from": dev_wallet})
# vault.balanceOf(dev_wallet)
# vault.withdraw(NFT_ETH_VALUE, dev_wallet, dev_wallet, {"from":dev_wallet})

nftGifts = NFTGifts.deploy(vault.address, {"from": dev_wallet})
tx8 = nftGifts.addNewGiftURI(URI_EXAMPLE, NFT_ETH_VALUE, {"from": dev_wallet})
tx9 = weth.approve(nftGifts.address, APPROVE_VALUE, {"from": dev_wallet})
CREATOR_ADDR = dev_wallet.address

weth.balanceOf(dev_wallet)
nftGifts.balanceOf(dev_wallet)
tx11 = nftGifts.mintGift(CREATOR_ADDR, URI_EXAMPLE, {"from": dev_wallet})
weth.balanceOf(dev_wallet)
nftGifts.balanceOf(dev_wallet)

vault.maxWithdraw(nftGifts)
nftGifts.getTokenIdCounter()
nftGifts.getAllURIs()
nftGifts.getEthValueOfGift(URI_EXAMPLE)
nftGifts.getTotalQtyOfGift(URI_EXAMPLE)
nftGifts.getGiftQtyOf(CREATOR_ADDR, URI_EXAMPLE)
nftGifts.getEthBalanceOfPerGift(CREATOR_ADDR, URI_EXAMPLE)
nftGifts.getEthBalanceOf(CREATOR_ADDR)
nftGifts.getTotalEthBalance()
nftGifts.isRedeemed(1)
nftGifts.getAllDonators()
nftGifts.getAllReceivers()


tx13 = nftGifts.redeemDonation(1, {"from": dev_wallet})
weth.balanceOf(dev_wallet)
nftGifts.balanceOf(dev_wallet)
nftGifts.isRedeemed(1)
