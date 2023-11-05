from fastapi import APIRouter

from realfans_api.schemas.users import UserProfile
from realfans_api.routes.helpers import get_user_info__by_address, get_user_info__by_username

router = APIRouter()


@router.get("/getUserInfo")
async def get_user_info(username: str) -> UserProfile:
    return await get_user_info__by_username(username)


@router.get("/getUserInfoByAddress")
async def get_user_info_by_address(address: str) -> UserProfile:
    return await get_user_info__by_address(address)


@router.post("/submit_twitter_handle")
async def submit_twitter_handle(address: str, twitter_handle: str, twitter_token: str) -> int:
    print(address)
    print(twitter_handle)
    print(twitter_token)
    return 1
