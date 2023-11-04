from .models import TwitterProfile, BadgeMinted, UserAdded, Donation, Redemption


class MyDatabase:
    twitter_profiles: dict[str, TwitterProfile]
    address_to_twitter: dict[str, str] = {}  # address, twitter handle
    twitter_to_address: dict[str, str] = {}  # reverse from above
    donations_sent: dict[str, Donation] = {}  # address, Donation
    donations_received: dict[str, Donation] = {}  # twitter handler, Donation
    quests_profile: dict[str, BadgeMinted] = {}  # address, BadgeMinted

    @staticmethod
    def add_twitter_profile(profile: TwitterProfile):
        ...

    @staticmethod
    def add_user_added(profile: UserAdded):
        ...

    @staticmethod
    def add_badge_minted(profile: BadgeMinted):
        ...

    @staticmethod
    def add_donation(profile: Donation):
        ...

    @staticmethod
    def add_redemption(profile: Redemption):
        ...
