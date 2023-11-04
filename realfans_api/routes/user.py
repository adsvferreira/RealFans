from fastapi import APIRouter

from realfans_api.data.models import TwitterProfile
from realfans_api.socialblade.api import SocialBladeAPI

router = APIRouter()

API = SocialBladeAPI()

cache: dict[str, TwitterProfile] = {}


@router.get("/getUserInfo")
async def get_user_info(username: str) -> TwitterProfile:
    username = username.lower()
    if username in cache:
        return cache[username]
    profile = await API.get_user_data(username)
    cache[username] = profile
    return profile
