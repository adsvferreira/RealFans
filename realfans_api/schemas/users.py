from dataclasses import field
from typing import Optional, Union
from pydantic.dataclasses import dataclass

from realfans_api.data.models import LeaderboardType, TwitterProfile, Donation, BadgeMinted


@dataclass
class BadgeMintedWithImage(BadgeMinted):
    image: str


@dataclass
class UserProfileStats:
    eth_sent: float = 0
    eth_received: float = 0
    ranks: dict[LeaderboardType, Union[int, None]] = field(default_factory=dict)
    quests_done: list[BadgeMintedWithImage] = field(default_factory=list)


@dataclass
class UserProfile(TwitterProfile):
    address: Optional[str] = None
    gifts_sent: list[Donation] = field(default_factory=list)
    gifts_received: list[Donation] = field(default_factory=list)
    stats: UserProfileStats = field(default_factory=UserProfileStats)
