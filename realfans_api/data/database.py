from .models import TwitterProfile, BadgeMinted, UserAdded, Donation, Redemption


class MyDatabase:
    twitter_profiles: dict[str, TwitterProfile] = {}  # username, TwitterProfile
    address_to_twitter: dict[str, str] = {}  # address, twitter handle
    twitter_to_address: dict[str, str] = {}  # reverse from above
    donations_sent: dict[str, list[Donation]] = {}  # address, Donation
    donations_received: dict[str, list[Donation]] = {}  # twitter handler, Donation
    quests_profile: dict[str, list[BadgeMinted]] = {}  # address, BadgeMinted

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
