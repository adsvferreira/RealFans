from brownie import accounts, config, network
from brownie import (
    SoulboundBadges,
)

BADGE_URI_EXAMPLE = "https://ipfs.io/ipfs/QmfTrPkKduncJvxCybkRTsUgFk6Y3fBnQrseGGbLZR9GSZ?filename=conservative.json"
BADGE_ETH_VALUE = 100_000_000_000_000_000  # 0.1 eth

dev_wallet = accounts.add(config["wallets"]["from_key_1"])
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
