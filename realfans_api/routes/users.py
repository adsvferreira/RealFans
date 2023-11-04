from fastapi import APIRouter
from dataclasses import asdict

from realfans_api.data.database import MyDatabase
from realfans_api.schemas.users import UserProfile
from realfans_api.socialblade.api import SocialBladeAPI

router = APIRouter()
API = SocialBladeAPI()


@router.get("/getUserInfo")
async def get_user_info(username: str) -> UserProfile:
    username = username.lower()
    if username in MyDatabase.twitter_profiles:
        profile = MyDatabase.twitter_profiles[username]
    else:
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


@router.post("/submit_twitter_handle")
async def submit_twitter_handle(address: str, twitter_token: str):
    ...
