# from data.models import Event
from realfans_api.data.database import MyDatabase

# from scripts.build_contracts import build_contracts


def execute():
    block = None
    while True:  # POG
        contracts = build_contracts()

        # Fetch User events
