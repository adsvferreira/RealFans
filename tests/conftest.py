import pytest
from typing import List, Dict
from docs.abis import erc20_abi
from brownie import config, network, Contract


@pytest.fixture()
def deposit_token() -> Contract:
    return Contract.from_abi(
        "ERC20",
        config["networks"][network.show_active()]["deposit_token_address"],
        erc20_abi,
    )
