from fastapi import APIRouter
from dataclasses import asdict

from realfans_api.schemas.users import UserProfile
from realfans_api.socialblade.api import SocialBladeAPI
from realfans_api.data.database import MyDatabase, TwitterProfile

router = APIRouter()
API = SocialBladeAPI()


@router.get("/getUserInfo")
async def get_user_info(username: str) -> UserProfile:
    username = username.lower()
    profile = MyDatabase.get_twitter_profile(username)
    if not profile:
        profile = await API.get_user_data(username)
        MyDatabase.add_twitter_profile(profile)

    gifts_received = MyDatabase.get_user_received_donations(username)
    gifts_sent = MyDatabase.get_user_sent_gifts_by_twitter(username)
    quests_done = MyDatabase.get_user_quests_done_by_twitter(username)
    address = MyDatabase.get_twitter_address(username)
    return UserProfile(
        address=address,
        gifts_received=gifts_received,
        gifts_sent=gifts_sent,
        quests_done=quests_done,
        **asdict(profile),
    )


@router.get("/getUserInfoByAddress")
async def get_user_info__by_address(address: str) -> UserProfile:
    username = MyDatabase.get_address_twitter(address)
    if username:
        profile: TwitterProfile = MyDatabase.get_twitter_profile(username)
    else:
        profile = TwitterProfile()

    gifts_received = []
    if username:
        gifts_received = MyDatabase.get_user_received_donations(username)

    gifts_sent = MyDatabase.get_user_sent_gifts(address)
    quests_done = MyDatabase.get_user_quests_done(address)
    return UserProfile(
        address=address,
        gifts_received=gifts_received,
        gifts_sent=gifts_sent,
        quests_done=quests_done,
        **asdict(profile),
    )


@router.post("/submit_twitter_handle")
async def submit_twitter_handle(address: str, twitter_token: str):
    ...
