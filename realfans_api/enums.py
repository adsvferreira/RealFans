from brownie import project, network

BROWNIE_PROJECT = project.load(".")
BROWNIE_PROJECT.load_config()
network.connect("arbitrum-main")