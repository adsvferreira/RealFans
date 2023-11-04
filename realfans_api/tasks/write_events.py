from brownie import chain
from realfans_api.data import database
from realfans_api.scripts.build_contracts import build_contracts




def execute(database: database.MyDatabase):
    to_block = None
    from_block = None
    contracts = build_contracts()
    while True:  # POG
        to_block = chain.height

        # Fetch user events
        users = contracts["users"]
        user_added_events = 
        database.add_multiple_entries
