from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass
class TwitterProfile:
    name: Optional[str] = None
    avatar: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    tweets: Optional[int] = None
    created_at: Optional[str] = None
