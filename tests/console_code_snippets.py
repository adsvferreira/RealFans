import pytest
from brownie import accounts, config, network
from brownie import (
    Users,
    SoulboundBadges,
)
dev_wallet = accounts.add(config["wallets"]["from_key_1"])
dev_address = dev_wallet.address

dev_wallet_2 = accounts.add(private_key=input("Private Key for personal wallet: "))
dev_address_2 = dev_wallet_2.address

################## SOULBOUND TESTS ##################

BADGE_URI_EXAMPLE = "https://ipfs.io/ipfs/QmfTrPkKduncJvxCybkRTsUgFk6Y3fBnQrseGGbLZR9GSZ?filename=conservative.json"
BADGE_ETH_VALUE = 100_000_000_000_000_000  # 0.1 eth

tx1 = SoulboundBadges.deploy({"from": dev_wallet})
soulboundBadges = SoulboundBadges[-1]
tx2 = soulboundBadges.addNewBadgeURI(BADGE_URI_EXAMPLE, BADGE_ETH_VALUE, {"from": dev_wallet})
tx3 = soulboundBadges.mintBadge(dev_wallet, BADGE_URI_EXAMPLE, {"from": dev_wallet})

soulboundBadges.getAllURIs()
soulboundBadges.getTokenIdCounter()
soulboundBadges.getEthValueOfBadge(BADGE_URI_EXAMPLE)
soulboundBadges.getTotalQtyOfBadge(BADGE_URI_EXAMPLE)
soulboundBadges.getBadgeQtyOf(dev_wallet, BADGE_URI_EXAMPLE)
soulboundBadges.getEthBalanceOfPerBadge(dev_wallet, BADGE_URI_EXAMPLE)
soulboundBadges.getEthBalanceOf(dev_wallet)
soulboundBadges.getTotalEthBalance()

################## USERS TESTS ##################

users_tx_1 = Users.deploy({"from": dev_wallet})
users = Users[-1]
twitter_handle = "1DeadPixel"

# Associate a twitter handle to an address
users_tx_2 = users.writeTwitterHandle(dev_address, twitter_handle, {"from": dev_wallet})

# Assert that the mapping from address to twitter handle is correct and vice versa
assert(users.getAddressFromTwitterHandle(twitter_handle) == dev_address)
assert(users.getTwitterHandleFromAddress(dev_address) == twitter_handle)

# Try associating another wallet to the same twitter handle and another twitter handle to the same address.
# Note: It's expected that both these transactions fail.
twitter_handle_2 = "random"
users.writeTwitterHandle(dev_address_2, twitter_handle, {"from": dev_wallet})
users.writeTwitterHandle(dev_address, twitter_handle_2, {"from": dev_wallet})

# Try writeTwitterHandle with a wallet that's not owner
# Note: The association doesn't exist but the wallet sending the transaction is not owner
users.writeTwitterHandle(dev_address_2, twitter_handle_2, {"from": dev_wallet_2})