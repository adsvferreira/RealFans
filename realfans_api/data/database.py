from typing import Optional
from .models import TwitterProfile, BadgeMinted, UserAdded, Donation, Redemption


class MyDatabase:
    twitter_profiles: dict[str, TwitterProfile] = {}  # username, TwitterProfile
    address_to_twitter: dict[str, str] = {}  # address, twitter handle
    twitter_to_address: dict[str, str] = {}  # reverse from above
    donations_sent: dict[str, list[Donation]] = {}  # address, Donation
    donations_received: dict[str, list[Donation]] = {}  # twitter handler, Donation
    quests_profile: dict[str, list[BadgeMinted]] = {}  # address, BadgeMinted

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

    @classmethod
    def add_donation(cls, donation: Donation):
        cls.donations_sent.setdefault(donation.sender, []).append(donation)
        cls.donations_received.setdefault(donation.receiver_twitter_handle, []).append(donation)

    @classmethod
    def add_redemption(cls, redemption: Redemption):
        for donation in cls.donations_received[redemption.receiver_twitter_handle]:
            if donation.redeemed:
                continue
            if donation.gift_uri != redemption.gift_token_uri:
                continue
            donation.redeemed = True
            break


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
