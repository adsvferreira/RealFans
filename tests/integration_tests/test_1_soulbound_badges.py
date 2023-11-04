import pytest
from helpers import check_network_is_mainnet_fork
from metadata.soulbound_uris import SOULBOUND_URIS
from brownie import (
    SoulboundBadges,
    config,
    network,
    accounts,
    exceptions,
)


dev_wallet = accounts.add(config["wallets"]["from_key_1"])
dev_wallet2 = accounts.add(config["wallets"]["from_key_2"])


def test_add_soulbound_uris():
    check_network_is_mainnet_fork()
    # Arrange
    soulbound_contract = SoulboundBadges.deploy({"from": dev_wallet})
    # Act
    for uri in SOULBOUND_URIS.values():
        soulbound_contract.addNewBadgeURI(uri, {"from": dev_wallet})
    # Assert
    assert len(soulbound_contract.getAllURIs()) == len(SOULBOUND_URIS)


def test_mint_badge():
    check_network_is_mainnet_fork()
    # Arrange
    soulbound_contract = SoulboundBadges[-1]
    uri = list(SOULBOUND_URIS.values())[0]
    initial_badge_count = soulbound_contract.getTotalQtyOfBadge(uri)
    initial_wallet_badge_count = soulbound_contract.getBadgeQtyOf(dev_wallet2, uri)
    initial_token_id_counter = soulbound_contract.getTokenIdCounter()
    # Act
    soulbound_contract.mintBadge(dev_wallet2, uri, {"from": dev_wallet})
    final_badge_count = soulbound_contract.getTotalQtyOfBadge(uri)
    final_wallet_badge_count = soulbound_contract.getBadgeQtyOf(dev_wallet2, uri)
    final_token_id_counter = soulbound_contract.getTokenIdCounter()
    # Assert
    assert final_badge_count == initial_badge_count + 1
    assert final_wallet_badge_count == initial_wallet_badge_count + 1
    assert final_token_id_counter == initial_token_id_counter + 1


def test_re_add_soulbound_uri():
    check_network_is_mainnet_fork()
    # Arrange
    soulbound_contract = SoulboundBadges[-1]
    uri = list(SOULBOUND_URIS.values())[0]
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        soulbound_contract.addNewBadgeURI(uri, {"from": dev_wallet})


def test_add_soulbound_uri_by_non_owner():
    check_network_is_mainnet_fork()
    # Arrange
    soulbound_contract = SoulboundBadges[-1]
    uri = "https://test_uri.json"
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        soulbound_contract.addNewBadgeURI(uri, {"from": dev_wallet2})


def test_mint_not_added_uri():
    check_network_is_mainnet_fork()
    # Arrange
    soulbound_contract = SoulboundBadges[-1]
    uri = "https://test_uri.json"
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        soulbound_contract.mintBadge(dev_wallet2, uri, {"from": dev_wallet})


def test_mint_badge_by_non_owner():
    check_network_is_mainnet_fork()
    # Arrange
    soulbound_contract = SoulboundBadges[-1]
    uri = list(SOULBOUND_URIS.values())[0]
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        soulbound_contract.mintBadge(dev_wallet2, uri, {"from": dev_wallet2})
