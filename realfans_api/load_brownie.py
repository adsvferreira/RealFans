import os
from dotenv import load_dotenv, find_dotenv
from brownie import project, network, accounts, config


load_dotenv(find_dotenv())

if not os.getenv("NETWORK_ID", ""):
    raise Exception("NETWORK_ID ENV VARIABLE NOT DEFINED")

BROWNIE_PROJECT = project.load(".")
BROWNIE_PROJECT.load_config()
network.connect(os.getenv("NETWORK_ID", ""))
OWNER_WALLET = accounts.add(config["wallets"]["from_key_1"])
