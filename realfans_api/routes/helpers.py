from typing import Optional
from dataclasses import asdict

from realfans_api.socialblade.api import SocialBladeAPI
from realfans_api.data.database import MyDatabase, TwitterProfile
from realfans_api.schemas.users import UserProfile, UserProfileStats

API = SocialBladeAPI()


def get_user_stats(username: Optional[str], address: Optional[str]) -> UserProfileStats:
    quests_done = []
    if address:
        quests_done = MyDatabase.get_user_quests_done(address)
    elif username and not quests_done:
        quests_done = MyDatabase.get_user_quests_done_by_twitter(username)

    eth_sent = MyDatabase.get_total_eth_gifted_by_address(address)
    eth_received = MyDatabase.get_total_eth_received_by_creator(username)
    ranks = MyDatabase.get_user_ranks(username, address)

    return UserProfileStats(eth_sent=eth_sent, eth_received=eth_received, ranks=ranks, quests_done=quests_done)


async def get_user_info__by_username(username: str) -> UserProfile:
    username = username.lower()
    profile = MyDatabase.get_twitter_profile(username)
    if not profile:
        profile = await API.get_user_data(username)
        if profile.name:
            MyDatabase.add_twitter_profile(profile)

    gifts_received = MyDatabase.get_user_received_donations(username)
    gifts_sent = MyDatabase.get_user_sent_gifts_by_twitter(username)
    address = MyDatabase.get_twitter_address(username)
    return UserProfile(
        address=address,
        gifts_received=gifts_received,
        gifts_sent=gifts_sent,
        stats=get_user_stats(username, address),
        **asdict(profile),
    )


async def get_user_info__by_address(address: str) -> UserProfile:
    username = MyDatabase.get_address_twitter(address)
    profile = None
    if username:
        profile = MyDatabase.get_twitter_profile(username)

    if not profile:
        profile = TwitterProfile()

    gifts_received = []
    if username:
        gifts_received = MyDatabase.get_user_received_donations(username)

    gifts_sent = MyDatabase.get_user_sent_gifts(address)
    return UserProfile(
        address=address,
        gifts_received=gifts_received,
        gifts_sent=gifts_sent,
        stats=get_user_stats(username, address),
        **asdict(profile),
    )
