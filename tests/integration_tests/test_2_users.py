import pytest
from helpers import check_network_is_mainnet_fork, NULL_ADDRESS
from brownie import (
    Users,
    config,
    accounts,
    exceptions,
)


dev_wallet = accounts.add(config["wallets"]["from_key_1"])
dev_wallet_handle = "1DeadPixel"
dev_wallet2 = accounts.add(config["wallets"]["from_key_2"])
dev_wallet_handle2 = "elonmusk"


def test_write_twitter_handle():
    check_network_is_mainnet_fork()
    # Arrange
    users = Users.deploy({"from": dev_wallet})
    initial_handle_from_address = users.getTwitterHandleFromAddress(dev_wallet)
    initial_address_from_handle = users.getAddressFromTwitterHandle(dev_wallet_handle)
    # Act
    users.writeTwitterHandle(dev_wallet, dev_wallet_handle, {"from": dev_wallet})
    final_handle_from_address = users.getTwitterHandleFromAddress(dev_wallet)
    final_address_from_handle = users.getAddressFromTwitterHandle(dev_wallet_handle)
    # Assert
    assert initial_handle_from_address == ""
    assert initial_address_from_handle == NULL_ADDRESS
    assert final_handle_from_address == dev_wallet_handle
    assert final_address_from_handle == dev_wallet.address


def test_re_write_twitter_handle():
    check_network_is_mainnet_fork()
    # Arrange
    users = Users[-1]
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        users.writeTwitterHandle(dev_wallet, dev_wallet_handle2, {"from": dev_wallet})


def test_write_already_used_twitter_handle():
    check_network_is_mainnet_fork()
    # Arrange
    users = Users[-1]
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        users.writeTwitterHandle(dev_wallet2, dev_wallet_handle, {"from": dev_wallet})


def test_write_twitter_handle_by_non_owner():
    check_network_is_mainnet_fork()
    # Arrange
    users = Users[-1]
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        users.writeTwitterHandle(dev_wallet2, dev_wallet_handle, {"from": dev_wallet})
