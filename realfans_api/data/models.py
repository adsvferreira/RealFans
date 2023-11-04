from enum import Enum
from typing import Optional
from pydantic.dataclasses import dataclass


class LeaderboardType(str, Enum):
    QUESTS = "QUESTS"
    DONATERS = "DONATERS"
    CREATORS = "CREATORS"


@dataclass
class TwitterProfile:
    username: str
    name: Optional[str] = None
    avatar: Optional[str] = None
    tweets: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None


@dataclass
class Donation:
    sender: str
    receiver_twitter_handle: str
    gift_uri: str
    eth_value: float
    redeemed: bool = False


@dataclass
class Redemption:
    sender: str
    receiver_twitter_handle: str
    gift_token_uri: str
    eth_value: float


@dataclass
class BadgeMinted:
    to_address: str
    badge_uri: str


@dataclass
class UserAdded:
    address: str
    twitter_handle: str