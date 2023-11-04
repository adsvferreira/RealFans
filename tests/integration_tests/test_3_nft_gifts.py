import pytest
from helpers import check_network_is_mainnet_fork, NULL_ADDRESS
from brownie import (
    NFTGifts,
    config,
    accounts,
    exceptions,
)


dev_wallet = accounts.add(config["wallets"]["from_key_1"])
dev_wallet_handle = "1DeadPixel"
dev_wallet2 = accounts.add(config["wallets"]["from_key_2"])
dev_wallet_handle2 = "elonmusk"


def test_add_gift_uri():
    pass


def test_donate_to_registred_account():
    pass


def test_donate_to_unregistred_account():
    pass


def test_redeem_from_registred_account():
    pass


def test_redeem_from_unregistred_account():
    pass


#################


def test_add_gift_uri_non_owner():
    pass


def test_re_add_gift_uri():
    pass


def test_donate_not_whitelisted_token_uri():
    pass


def test_redeem_from_not_allowed_registred_account():
    pass


def test_redeem_from_not_allowed_unregistred_account():
    pass
