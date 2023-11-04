from fastapi import APIRouter

from realfans_api.data.models import TwitterProfile
from realfans_api.socialblade.api import SocialBladeAPI

router = APIRouter()

API = SocialBladeAPI()


@router.get("/getUserInfo")
async def get_user_info(username: str) -> TwitterProfile:
    return await API.get_user_data(username)
