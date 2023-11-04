import pytest
from brownie import accounts, config, network

NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
CONSOLE_SEPARATOR = "--------------------------------------------------------------------------"


def get_account_from_pk(index: int) -> object:
    return accounts.add(config["wallets"][f"from_key_{index}"])


def check_network_is_mainnet_fork():
    if network.show_active() == "development" or "fork" not in network.show_active():
        pytest.skip("Only for mainnet-fork testing!")
