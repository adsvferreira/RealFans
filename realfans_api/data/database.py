from typing import Optional, Union

from badge_minter.minter import BadgeMinter
from realfans_api.data.models import TwitterProfile, BadgeMinted, UserAdded, Donation, Redemption, LeaderboardType


class MyDatabase:
    twitter_profiles: dict[str, TwitterProfile] = {}  # username, TwitterProfile
    address_to_twitter: dict[str, str] = {}  # address, twitter handle
    twitter_to_address: dict[str, str] = {}  # reverse from above
    donations_sent: dict[str, list[Donation]] = {}  # address, Donation
    donations_received: dict[str, list[Donation]] = {}  # twitter handler, Donation
    quests_profile: dict[str, list[BadgeMinted]] = {}  # address, BadgeMinted
    leaderboards: dict[LeaderboardType, dict[str, int]] = {
        LeaderboardType.QUESTS: {},
        LeaderboardType.CREATORS: {},
        LeaderboardType.DONATERS: {},
    }

    @classmethod
    def get_twitter_profile(cls, twitter_handle: str) -> Optional[TwitterProfile]:
        return cls.twitter_profiles.get(twitter_handle)

    @classmethod
    def get_twitter_address(cls, twitter_handle: str) -> Optional[str]:
        return cls.twitter_to_address.get(twitter_handle)

    @classmethod
    def get_address_twitter(cls, address: str) -> Optional[str]:
        return cls.address_to_twitter.get(address)

    @classmethod
    def get_user_received_donations(cls, twitter_handle: str) -> list[Donation]:
        return cls.donations_received.get(twitter_handle, [])

    @classmethod
    def get_user_sent_gifts(cls, address: str) -> list[Donation]:
        return cls.donations_sent.get(address, [])

    @classmethod
    def get_user_sent_gifts_by_twitter(cls, twitter_handle: str) -> list[Donation]:
        address = cls.twitter_to_address.get(twitter_handle)
        if not address:
            return []
        return cls.get_user_sent_gifts(address)

    @classmethod
    def get_user_quests_done(cls, address: str) -> list[BadgeMinted]:
        return cls.quests_profile.get(address, [])

    @classmethod
    def get_total_eth_received_by_creator(cls, twitter_handle: Optional[str]) -> float:
        if not twitter_handle:
            return 0
        return sum(donation.eth_value for donation in cls.donations_received.get(twitter_handle, []))

    @classmethod
    def get_user_ranks(
        cls, twitter_handle: Optional[str], address: Optional[str]
    ) -> dict[LeaderboardType, Union[int, None]]:
        return {
            LeaderboardType.QUESTS: cls.leaderboards[LeaderboardType.QUESTS].get(address),
            LeaderboardType.CREATORS: cls.leaderboards[LeaderboardType.CREATORS].get(twitter_handle),
            LeaderboardType.DONATERS: cls.leaderboards[LeaderboardType.DONATERS].get(address),
        }

    @classmethod
    def get_total_eth_gifted_by_address(cls, address: Optional[str]) -> float:
        if not address:
            return 0
        return sum(donation.eth_value for donation in cls.donations_sent.get(address, []))

    @classmethod
    def get_user_quests_done_by_twitter(cls, twitter_handle: str) -> list[BadgeMinted]:
        address = cls.twitter_to_address.get(twitter_handle)
        if not address:
            return []
        return cls.get_user_quests_done(address)

    @classmethod
    def add_twitter_profile(cls, profile: TwitterProfile):
        cls.twitter_profiles[profile.username] = profile

    @classmethod
    def add_user_added(cls, user_added: UserAdded):
        cls.address_to_twitter[user_added.address] = user_added.twitter_handle
        cls.twitter_to_address[user_added.twitter_handle] = user_added.address

    @classmethod
    def add_badge_minted(cls, badge_minted: BadgeMinted):
        cls.quests_profile.setdefault(badge_minted.to_address, []).append(badge_minted)
        cls.compute_quests_leaderboard()

    @classmethod
    def add_donation(cls, donation: Donation):
        cls.donations_sent.setdefault(donation.sender, []).append(donation)
        cls.donations_received.setdefault(donation.receiver_twitter_handle, []).append(donation)
        cls.compute_leaderboard()
        BadgeMinter.queue_mint_badge(donation.sender, cls.donations_sent[donation.sender])

    @classmethod
    def add_redemption(cls, redemption: Redemption):
        for donation in cls.donations_received[redemption.receiver_twitter_handle]:
            if donation.redeemed:
                continue
            if donation.gift_uri != redemption.gift_token_uri:
                continue
            donation.redeemed = True
            break

    @classmethod
    def compute_leaderboard(cls):
        creators_leaderboard: dict[str, float] = {}
        donaters_leaderboard: dict[str, float] = {}

        for donations in cls.donations_received.values():
            for donation in donations:
                creators_leaderboard[donation.receiver_twitter_handle] = (
                    creators_leaderboard.get(donation.receiver_twitter_handle, 0) + donation.eth_value
                )

        for donations in cls.donations_sent.values():
            for donation in donations:
                donaters_leaderboard[donation.sender] = (
                    donaters_leaderboard.get(donation.sender, 0) + donation.eth_value
                )

        sorted_creators = {
            k: v for k, v in sorted(creators_leaderboard.items(), key=lambda item: item[1], reverse=True)
        }
        sorted_donaters = {
            k: v for k, v in sorted(donaters_leaderboard.items(), key=lambda item: item[1], reverse=True)
        }

        cls.leaderboards[LeaderboardType.CREATORS] = {
            handle: rank for rank, handle in enumerate(sorted_creators, start=1)
        }
        cls.leaderboards[LeaderboardType.DONATERS] = {
            address: rank for rank, address in enumerate(sorted_donaters, start=1)
        }

    @classmethod
    def compute_quests_leaderboard(cls):
        quests_leaderboard: dict[str, int] = {address: len(badges) for address, badges in cls.quests_profile.items()}
        sorted_quests_leaderboard = {
            k: rank
            for rank, (k, _) in enumerate(
                sorted(quests_leaderboard.items(), key=lambda item: item[1], reverse=True), start=1
            )
        }
        cls.leaderboards[LeaderboardType.QUESTS] = sorted_quests_leaderboard


MyDatabase.add_twitter_profile(
    TwitterProfile(
        username="elonmusk",
        name="Elon Musk",
        tweets=32845,
        followers=162094340,
        following=474,
        created_at="Jun 2nd, 2009",
        avatar="https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO.jpg",
    )
)

MyDatabase.add_donation(
    Donation(
        sender="0x",
        receiver_twitter_handle="elonmusk",
        gift_uri="ipfs://bafybeiem3hww2qkwzei3r62jx2xu25nax6zaaunaqag6uyaiuyd2hwgxba/Bronze.json",
        eth_value=1,
        redeemed=False,
    )
)

MyDatabase.add_donation(
    Donation(
        sender="0x",
        receiver_twitter_handle="elonmusk",
        gift_uri="ipfs://bafybeiem3hww2qkwzei3r62jx2xu25nax6zaaunaqag6uyaiuyd2hwgxba/Silver.json",
        eth_value=10,
        redeemed=False,
    )
)

MyDatabase.add_user_added(
    UserAdded(
        address="0x1",
        twitter_handle="elonmusk",
    )
)

MyDatabase.add_redemption(
    Redemption(
        sender="0x1",
        receiver_twitter_handle="elonmusk",
        gift_token_uri="ipfs://bafybeiem3hww2qkwzei3r62jx2xu25nax6zaaunaqag6uyaiuyd2hwgxba/Bronze.json",
        eth_value=1,
    )
)
