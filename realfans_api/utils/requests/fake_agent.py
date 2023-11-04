import os
import random
import string
import aiohttp
from typing import Optional
from user_agent import generate_navigator
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "DNT": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}


PROXY = os.environ.get("PROXY")
if PROXY:
    country_index_start = PROXY.index("country-")
    COUNTRY_FLAG = PROXY[country_index_start : country_index_start + 11]


DEFAULT_TIMEOUT_REQUESTS = 15
TIMEOUT = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT_REQUESTS)


def generate_fake_agent() -> dict[str, str]:
    navigator = generate_navigator(device_type=["all"])
    headers = dict(DEFAULT_HEADERS)
    headers["User-Agent"] = navigator["user_agent"]

    # available navigator_id = ie, firefox, chrome
    if navigator["navigator_id"] == "chrome":
        # only chromium uses this headers
        chrome_version = navigator["build_version"].split(".")[0]
        platform = navigator["platform"].split(" ")[0]
        is_phone = int(platform == "Android")
        platform = {
            "X11;": "Linux",
            "Linux": "Android",
            "MacIntel": "macOS",
        }.get(platform, platform)
        headers[
            "sec-ch-ua"
        ] = f'" Not A;Brand";v="99", "Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}"'
        headers["sec-ch-ua-mobile"] = f"?{is_phone}"
        headers["sec-ch-ua-platform"] = f'"{platform}"'
    return headers


def generate_proxy(change_country=False) -> Optional[str]:
    if not PROXY:
        return None
    HTTP = "http://"
    proxy = HTTP + PROXY.replace("12345", "".join(random.choices(string.ascii_uppercase + string.digits, k=6)))

    if change_country:
        random_country = random.choice(
            ["gb", "nl", "pt", "es", "it", "fr", "de", "cz", "ie", "be", "lu", "at", "pl", "fi", "se"]
        )  # europe country codes

        proxy = proxy.replace(COUNTRY_FLAG, f"country-{random_country}:")
    return proxy
