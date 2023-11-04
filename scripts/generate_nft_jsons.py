import json
from metadata.nft_metadata import *

FILE_PATH = "./metadata/files"

def generate_json(nft_dict: dict):
    with open(f"{FILE_PATH}/{nft_dict['name']}.json", "w") as file:
        json.dump(nft_dict, file)
        
def main():
    generate_json(nft_bronze)
    generate_json(nft_silver)
    generate_json(nft_gold)
    generate_json(nft_platinum)
    generate_json(nft_diamond)