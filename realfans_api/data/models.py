from typing import Optional
from enum import Enum, auto
from pydantic.dataclasses import dataclass


class LeaderboardType(str, Enum):
    DONATERS = auto()
    QUESTS = auto()
    CREATORS = auto()


@dataclass
class TwitterProfile:
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
