import re
import aiohttp
from typing import Optional

from realfans_api.data.models import TwitterProfile
from realfans_api.utils.requests.api_interface import APIInterfaceAsync, ExternalAPIException, ForbiddenException


class Parsers:
    name = re.compile(r"<h2.*?>(.*?)<a href=")
    followers = re.compile(r"Followers</span><br>\s*<span style=\"font-weight: bold;\">([\d,]+)</span>")
    following = re.compile(r"Following</span><br>\s*<span style=\"font-weight: bold;\">([\d,]+)</span>")
    avatar = re.compile(r"<img id=\"YouTubeUserTopInfoAvatar\" src=\"(.*?)\" alt=")
    tweets = re.compile(r"Tweets</span><br>\s*<span style=\"font-weight: bold;\">([\d,]+)</span>")
    created_at = re.compile(r"User Created</span><br>\s*<span style=\"font-weight: bold;\">(.*?)</span>")
    invalid_response = []  # [re.compile(r"")]


class SocialBladeAPI(APIInterfaceAsync):
    ROOT_URL = "https://socialblade.com/"

    async def get_user_data(self, username: str) -> TwitterProfile:
        while 1:
            try:
                url, status, html = await self.request(f"twitter/user/{username}", "GET")
            except ForbiddenException:
                print(f"Forbidden request on {username}")
                continue

        requested_url = f"{self.ROOT_URL}twitter/user/{username}"
        if self.__was_invalid_request(url, requested_url, status):
            raise ExternalAPIException(
                f"Failed request, status: {status}, requested url: {requested_url}\n\nHtml: {html}"
            )
        if self.__check_if_invalid(html):
            raise ExternalAPIException(f"Invalid data.\n\nHtml: {html}")

        return TwitterProfile(
            username=username.lower(),
            name=self.parse_name(html),
            avatar=self.parse_avatar(html),
            followers=self.parse_followers(html),
            following=self.parse_following(html),
            tweets=self.parse_tweets(html),
            created_at=self.parse_created_at(html),
        )

    async def callback(self, response: aiohttp.ClientResponse) -> tuple[str, int, str]:
        return str(response.url), response.status, await response.text()

    def parse_followers(self, html: str) -> Optional[int]:
        return self.__parse_int(Parsers.followers, html)

    def parse_following(self, html: str) -> Optional[int]:
        return self.__parse_int(Parsers.following, html)

    def parse_tweets(self, html: str) -> Optional[int]:
        return self.__parse_int(Parsers.tweets, html)

    def parse_name(self, html: str) -> Optional[str]:
        return self.__parse_str(Parsers.name, html)

    def parse_avatar(self, html: str) -> Optional[str]:
        return self.__parse_str(Parsers.avatar, html)

    def parse_created_at(self, html: str) -> Optional[str]:
        return self.__parse_str(Parsers.created_at, html)

    def __check_if_invalid(self, html: str) -> bool:
        return any(pattern.search(html) for pattern in Parsers.invalid_response)

    def __parse_int(self, pattern: re.Pattern, html: str) -> Optional[int]:
        if match := pattern.search(html):
            return int(self.get_match(match).replace(",", ""))
        return None

    def __parse_str(self, pattern: re.Pattern, html: str) -> Optional[str]:
        if match := pattern.search(html):
            return self.get_match(match)
        return None

    def get_match(self, match: re.Match) -> str:
        try:
            return match[1]
        except:  # quickfix - see explanation on comment below at #COMMENT
            return match[0]

    def __was_invalid_request(self, url: str, requested_url: str, status_code: int) -> bool:
        if status_code >= 400:  # status code != 200
            return True
        return requested_url != url  # original url is not the requested url, this means redirect to a default page


# COMMENT
"""
on this regex:
    (?<=<name>).+(?=<\/name>)
I have to use match.group(0)

And on this regex:
    <h1 class="username-avatar hero-title">(.*?)</h1>
I have to use match.group(1)

Can you explain me why?
==============================================================================
Certainly! The difference lies in the use of capture groups in the second regex.

In the first regex (?<=<name>).+(?=<\/name>), you are using lookbehind (?<=...) and lookahead (?=...) assertions. These assertions don't create capture groups but only assert that the pattern before or after the match must be present. So, when you use match.group(0), it returns the entire match, which is the content between the <title> tags.

In the second regex <h1 class="username-avatar hero-title">(.*?)</h1>, you are using a capture group, which is denoted by the parentheses (.*?). This capture group is used to capture the content between the <h1> tags. Here, match.group(0) would return the entire match, including the <h1> tags, whereas match.group(1) returns only the content of the first (and only) capture group, i.e., the content between the <h1> tags.
"""
