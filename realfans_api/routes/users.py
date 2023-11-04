from fastapi import APIRouter

from realfans_api.data.database import MyDatabase
from realfans_api.data.models import TwitterProfile
from realfans_api.socialblade.api import SocialBladeAPI

router = APIRouter()
API = SocialBladeAPI()


@router.get("/getUserInfo")
async def get_user_info(username: str) -> TwitterProfile:
    username = username.lower()
    if username in MyDatabase.twitter_profiles:
        return MyDatabase.twitter_profiles[username]
    profile = await API.get_user_data(username)
    MyDatabase.add_twitter_profile(profile)
    return profile


@router.post("/submit_twitter_handle")
async def submit_twitter_handle(address: str, twitter_token: str):
    ...
