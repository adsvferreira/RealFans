from brownie import chain
from data.models import Event
from data.database import my_database
from scripts.build_contracts import build_contracts



def execute():
    from_block = None
    to_block = "latest"
    
    while True: # POG
        
        contracts = build_contracts()

        # Fetch User events
        users = contracts["users"]

