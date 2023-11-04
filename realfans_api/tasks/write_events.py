import os
from brownie import chain, network
from realfans_api.data import database
from realfans_api.scripts.build_contracts import build_contracts




def execute(database: database.MyDatabase):
    to_block = None
    from_block = 147050000  # Contracts deployed after this block 147050037
    network_id = os.getenv("NETWORK_ID", "")  # DEFAULT VALUE SHOULD NEVER BE USED
    contracts = build_contracts(network_id)
    while True:  # POG
        to_block = chain.height
        # Fetch user events
        users = contracts["users"]
        user_added_events = users.events.UserAdded.createFilter(fromBlock=from_block, to_block=to_block).get_all_entries()
        
