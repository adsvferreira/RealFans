from pydantic.dataclasses import dataclass

from realfans_api.schemas.users import UserProfile
from realfans_api.data.models import LeaderboardType


@dataclass
class LeaderBoardRank:
    rank: int
    value: int
    profile: UserProfile


@dataclass
class LeaderBoardRanks:
    type: LeaderboardType
    ranks: list[LeaderBoardRank]
