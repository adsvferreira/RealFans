import pytest
from brownie import accounts, config, network
from docs.abis import erc20_abi

dev_wallet = accounts.add(config["wallets"]["from_key_1"])
dev_wallet2 = accounts.add(config["wallets"]["from_key_2"])

URI_EXAMPLE = "https://ipfs.io/ipfs/QmfTrPkKduncJvxCybkRTsUgFk6Y3fBnQrseGGbLZR9GSZ?filename=conservative.json"
NFT_ETH_VALUE = 100_000_000_000_000  # 0.0001 weth
APPROVE_VALUE = 999_999_999_999_999_999_999_999_999_999
CREATOR_ADDR = "0xC55489B0Da14D81725509a03cF0Eb86a0a23D8eb"

asset = config["networks"][network.show_active()]["deposit_asset"]
vault_name = "Real Fans Community Pool"
vault_symbol = "RFCP"
weth = Contract.from_abi("ERC20", config["networks"][network.show_active()]["deposit_asset"], erc20_abi)

################## SOULBOUND TESTS ##################

# tx1 = SoulboundBadges.deploy({"from": dev_wallet})
# soulboundBadges = SoulboundBadges[-1]
# tx2 = soulboundBadges.addNewBadgeURI(URI_EXAMPLE, NFT_ETH_VALUE, {"from": dev_wallet})
# tx3 = soulboundBadges.mintBadge(dev_wallet, URI_EXAMPLE, {"from": dev_wallet})

soulboundBadges.getAllURIs()
soulboundBadges.getTokenIdCounter()
soulboundBadges.getTotalQtyOfBadge(URI_EXAMPLE)
soulboundBadges.getBadgeQtyOf(dev_wallet, URI_EXAMPLE)


################## USERS TESTS ##################

users_tx_1 = Users.deploy({"from": dev_wallet})
users = Users[-1]
twitter_handle = "1DeadPixel"

# Associate a twitter handle to an address
users_tx_2 = users.writeTwitterHandle(dev_wallet, twitter_handle, {"from": dev_wallet})

# Assert that the mapping from address to twitter handle is correct and vice versa
assert users.getAddressFromTwitterHandle(twitter_handle) == dev_wallet
assert users.getTwitterHandleFromAddress(dev_wallet) == twitter_handle

# Try associating another wallet to the same twitter handle and another twitter handle to the same address.
# Note: It's expected that both these transactions fail.
twitter_handle_2 = "random"
users.writeTwitterHandle(dev_wallet_2, twitter_handle, {"from": dev_wallet})
users.writeTwitterHandle(dev_wallet, twitter_handle_2, {"from": dev_wallet})

# Try writeTwitterHandle with a wallet that's not owner
# Note: The association doesn't exist but the wallet sending the transaction is not owner
users.writeTwitterHandle(dev_address_2, twitter_handle_2, {"from": dev_wallet_2})

################################################################

################## COMMUNITY VAULT TESTS ##################

vault = CommunityVault.deploy(asset, vault_name, vault_symbol, {"from": dev_wallet})
# tx5 = weth.approve(vault.address, APPROVE_VALUE, {"from": dev_wallet})
# tx6 = vault.deposit(100_000, dev_wallet, {"from": dev_wallet})
# vault.balanceOf(dev_wallet)
# vault.withdraw(NFT_ETH_VALUE, dev_wallet, dev_wallet, {"from":dev_wallet})


################## NFT TESTS ##################

nftGifts = NFTGifts.deploy(vault.address, {"from": dev_wallet})
tx8 = nftGifts.addNewGiftURI(URI_EXAMPLE, NFT_ETH_VALUE, {"from": dev_wallet})
tx9 = weth.approve(nftGifts.address, APPROVE_VALUE, {"from": dev_wallet})
CREATOR_ADDR = dev_wallet.address

weth.balanceOf(dev_wallet)
nftGifts.balanceOf(dev_wallet)
# mint to registred account
tx11 = nftGifts.mintGift(twitter_handle, URI_EXAMPLE, {"from": dev_wallet})
weth.balanceOf(dev_wallet)
vault.maxWithdraw(nftGifts)

nftGifts.balanceOf(dev_wallet)
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

# mint to unregistred account
tx12 = nftGifts.mintGift("elonmusk", URI_EXAMPLE, {"from": dev_wallet})
nftGifts.getGiftQtyOfUnclaimedAccount("elonmusk", URI_EXAMPLE)
nftGifts.getAllDonators()
nftGifts.getAllReceivers()
nftGifts.getAllUnclaimedAccountReceivers()

# redeem registred account donation
weth.balanceOf(dev_wallet)
tx13 = nftGifts.redeemDonation(1, {"from": dev_wallet})
weth.balanceOf(dev_wallet)
nftGifts.balanceOf(dev_wallet)
nftGifts.isRedeemed(1)

# add wallet address to "elonmusk" twitter handle
tx14 = users.writeTwitterHandle(dev_wallet2, "elonmusk", {"from": dev_wallet})

# redeem new registred account with previously sent donation
weth.balanceOf(dev_wallet2)
tx15 = nftGifts.redeemDonationsToUnclaimedAccount(URI_EXAMPLE, {"from": dev_wallet2})
weth.balanceOf(dev_wallet2)
