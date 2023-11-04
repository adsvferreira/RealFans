import json
from metadata.soulbound_metadata import *

FILE_PATH = "./metadata/files/soulbound"

def generate_json(nft_dict: dict):
    with open(f"{FILE_PATH}/{nft_dict['name'].replace(' ', '')}.json", "w") as file:
        json.dump(nft_dict, file)

def main():
    generate_json(soulbound_all_nfts)
