import json
from metadata.soulbound_metadata import *

FILE_PATH = "./metadata/files/soulbound"

def generate_json(nft_dict: dict):
    with open(f"{FILE_PATH}/{nft_dict['name'].replace(' ', '')}.json", "w") as file:
        json.dump(nft_dict, file)

def main():
    generate_json(soulbound_donate_1)
    generate_json(soulbound_donate_2)
    generate_json(soulbound_donate_3)
    generate_json(soulbound_people_1)
    generate_json(soulbound_people_2)
    generate_json(soulbound_people_3)
    generate_json(soulbound_fan_1)
    generate_json(soulbound_fan_2)
    generate_json(soulbound_fan_3)
    generate_json(soulbound_eth_1)
    generate_json(soulbound_eth_2)
    generate_json(soulbound_eth_3)
    generate_json(soulbound_all_nfts)
