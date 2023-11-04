import os
from brownie import project, network

if not os.getenv("NETWORK_ID", ""):
    raise Exception("NETWORK_ID ENV VARIABLE NOT DEFINED")

BROWNIE_PROJECT = project.load(".")
BROWNIE_PROJECT.load_config()
network.connect(os.getenv("NETWORK_ID", ""))