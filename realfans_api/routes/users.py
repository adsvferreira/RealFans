from fastapi import APIRouter

from twitter.validator import UserValidator
from realfans_api.schemas.users import UserProfile
from realfans_api.load_brownie import BROWNIE_PROJECT, OWNER_WALLET
from realfans_api.routes.helpers import get_user_info__by_address, get_user_info__by_username

router = APIRouter()


@router.get("/getUserInfo")
async def get_user_info(username: str) -> UserProfile:
    return await get_user_info__by_username(username)


@router.get("/getUserInfoByAddress")
async def get_user_info_by_address(address: str) -> UserProfile:
    return await get_user_info__by_address(address)


@router.post("/submit_twitter_handle")
async def submit_twitter_handle(address: str, twitter_handle: str, twitter_token: str) -> dict:
    try:
        if not UserValidator.validate_handle_by_token(twitter_handle, twitter_token):
            return {"success": False, "message": "Failed tx"}
        print(f"Twitter to wallet assoaction => {address}:{twitter_handle}")

        users_contract = BROWNIE_PROJECT.Users.at("0xf07CDD1D9cc628F4a28d8a63D52a5aF41311ca7B")
        users_contract.writeTwitterHandle(address, twitter_handle, {"from": OWNER_WALLET})
        return {"success": True, "message": "Ok"}

    except Exception as exc:
        import traceback

        traceback.print_exc()
        print(f"[{str(type(exc))}] Failed wallet twitter association => {address}:{twitter_handle}")
        return {"success": False, "message": "Failed tx"}
