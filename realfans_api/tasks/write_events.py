import os
import time
from brownie import chain, network
from realfans_api.tasks.helpers import event_parser
from realfans_api.data.database import MyDatabase as my_database
from realfans_api.scripts.build_contracts import build_contracts




def execute():
    print("STARTED")
    to_block = 0
    from_block = 147050000
    network_id = os.getenv("NETWORK_ID", "")  # DEFAULT VALUE SHOULD NEVER BE USED
    contracts = build_contracts(network_id)
    while True:  # POG
        to_block = chain.height
        if to_block > from_block:
            # Fetch and write user events
            users = contracts["users"]
            user_added_events = [event_parser.parse_user_added_event(event) for event in users.events.userAdded.createFilter(fromBlock=from_block, toBlock=to_block).get_all_entries()]
            my_database.add_multiple_entries(my_database.add_user_added, user_added_events)
        
            # Fetch and write NFT events
            nft = contracts["nft"]
            nft_donation_events = [event_parser.parse_donation_event(event) for event in nft.events.Donation.createFilter(fromBlock=from_block, toBlock=to_block).get_all_entries()]
            my_database.add_multiple_entries(my_database.add_donation, nft_donation_events)
            nft_redemption_events = [event_parser.parse_redemption_event(event) for event in nft.events.Redemption.createFilter(fromBlock=from_block, toBlock=to_block).get_all_entries()]
            my_database.add_multiple_entries(my_database.add_redemption, nft_redemption_events)

            # Fetch and write Soulbound events
            soulbound = contracts["soulbound"]
            soulbound_mint_events = [event_parser.parse_badge_minted_event(event) for event in soulbound.events.BadgeMinted.createFilter(fromBlock=from_block, toBlock=to_block).get_all_entries()]
            my_database.add_multiple_entries(my_database.add_badge_minted, soulbound_mint_events)

            if nft_redemption_events:
                print("DONATIONS_RECEIVED")
                print(nft_redemption_events)
                print()

            if nft_donation_events:
                print("DONATIONS_SENT")
                print(nft_donation_events)
                print()

            if user_added_events:
                print("TWITTER_TO_ADDRESS")
                print(user_added_events)
                print()

            if soulbound_mint_events:
                print("SOULBOUND MINTED")
                print(soulbound_mint_events)
                print()
            

        time.sleep(10)
        from_block = to_block
        