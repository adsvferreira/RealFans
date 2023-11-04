from data.models import Event
from data.database import my_database
from scripts.build_contracts import build_contracts

def execute():
    block = None
    while True: # POG
        contracts = build_contracts()

        # Fetch User events 