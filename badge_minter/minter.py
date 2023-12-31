from time import sleep
from typing import Any
from threading import Thread

from realfans_api.data.models import Donation
from metadata.soulbound_metadata import all_badges
from metadata.soulbound_uris import SOULBOUND_URIS
from realfans_api.load_brownie import BROWNIE_PROJECT, OWNER_WALLET


class BadgeMinter:
    @classmethod
    def queue_mint_badge(cls, address: str, donations: list[Donation]):
        thread = Thread(target=cls.mint_badge, args=(address, donations), daemon=True)
        thread.start()

    @classmethod
    def mint_badge(cls, address: str, donations: list[Donation]):
        if address == "0x":
            return
        sleep(10)

        from realfans_api.data.database import MyDatabase

        already_aquired_badges = {badge.badge_uri for badge in MyDatabase.quests_profile.get(address, [])}

        stats: dict[str, Any] = {}
        stats["donation_count"] = len(donations)
        stats["donation_unique_count"] = len({donation.receiver_twitter_handle for donation in donations})
        stats["donation_amount"] = sum(donation.eth_value for donation in donations)
        stats["donate_all_tiers"] = len({donation.gift_uri for donation in donations}) == 5

        donations_to_unique_users: dict[str, int] = {}
        for donation in donations:
            donations_to_unique_users.setdefault(donation.receiver_twitter_handle, 0)
            donations_to_unique_users[donation.receiver_twitter_handle] += 1

        stats["donation_repeat_count"] = max(donations_to_unique_users.values())

        for badge in all_badges.values():
            badge_id = SOULBOUND_URIS[badge["id"]]
            if badge_id in already_aquired_badges:
                print(f"{badge_id} already adquired, skipping...")
                continue

            mint_badge = True
            requirements = badge["requires"]
            for key, requirement_value in requirements.items():
                if key == "donation_amount":
                    if not (stats[key] >= requirement_value):
                        mint_badge = False
                        break
                    continue
                if not (stats[key] == requirement_value):
                    mint_badge = False
                    break

            if mint_badge:
                cls._mint_badge(address, badge)

    @classmethod
    def _mint_badge(cls, address: str, badge: dict):
        try:
            print(f"Minting badge to {address}")
            soulbound_contract = BROWNIE_PROJECT.SoulboundBadges.at(get_network_info_from_file()["soulbound_address"])

            badge_id = SOULBOUND_URIS[badge["id"]]
            try:
                soulbound_contract.mintBadge(address, badge_id, {"from": OWNER_WALLET})
            except RuntimeError:
                sleep(1)
                soulbound_contract.mintBadge(address, badge_id, {"from": OWNER_WALLET})
        except Exception as exc:
            import traceback

            if not isinstance(exc, ImportError):
                traceback.print_exc()
            print(f"[{str(type(exc))}] Failed Mint Quest NFT => {address}:{badge['requires']}")
