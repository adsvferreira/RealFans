from typing import Optional
from dataclasses import field
from pydantic.dataclasses import dataclass

from realfans_api.data.models import TwitterProfile, Donation, BadgeMinted


@dataclass
class UserProfile(TwitterProfile):
    address: Optional[str] = None
    gifts_sent: list[Donation] = field(default_factory=list)
    gifts_received: list[Donation] = field(default_factory=list)
    quests_done: list[BadgeMinted] = field(default_factory=list)
