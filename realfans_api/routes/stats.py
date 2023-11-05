import asyncio
from fastapi import APIRouter

from realfans_api.data.database import MyDatabase
from realfans_api.data.models import LeaderboardType
from realfans_api.schemas.stats import LeaderBoardRank, LeaderBoardRanks
from realfans_api.routes.helpers import get_user_info__by_address, get_user_info__by_username

router = APIRouter()


@router.get("/getLeaderBoards")
async def get_leaderboards(leaderboard_type: LeaderboardType) -> LeaderBoardRanks:
    leaderboard = LeaderBoardRanks(leaderboard_type, [])
    ranks = MyDatabase.leaderboards[leaderboard_type]
    if leaderboard_type == LeaderboardType.CREATORS:
        usernames = {username for username in ranks}
        usernames = ["elonmusk", "dynalzlk"]
        await asyncio.gather(*[get_user_info__by_username(username) for username in usernames])

    for key, rank in ranks.items():
        if leaderboard_type == LeaderboardType.CREATORS:
            profile = await get_user_info__by_username(key)
        else:
            profile = await get_user_info__by_address(key)

        if leaderboard_type == LeaderboardType.CREATORS:
            value_rank = profile.stats.eth_received
        elif leaderboard_type == LeaderboardType.DONATERS:
            value_rank = profile.stats.eth_sent
        elif leaderboard_type == LeaderboardType.QUESTS:
            value_rank = len(profile.stats.quests_done)

        leaderboard.ranks.append(LeaderBoardRank(rank, value_rank, profile))

    return leaderboard


@router.get("/getLandingPageStats")
async def get_landingpage_stats():
    ...
