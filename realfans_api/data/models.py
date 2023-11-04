from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass
class TwitterProfile:
    name: Optional[str] = None
    avatar: Optional[str] = None
    tweets: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None

@dataclass
class Transfer:
    from_address: str
    to_address: str
    value: int

@dataclass
class Approval:
    owner: str
    spender: str
    value: int

@dataclass
class Donation:
    sender: str
    to_address: str
    receiver_twitter_handle: str
    donator_twitter_handle: str
    gift_uri: str
    eth_value: int

@dataclass
class Redemption:
    sender: str
    receiver_twitter_handle: str
    gift_token_uri: str
    eth_value: int

@dataclass
class BadgeMinted:
    to_address: str
    badge_uri: str

@dataclass
class UserAdded:
    address: str
    twitter_handle: str