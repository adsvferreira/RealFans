import sys
import aiohttp
import asyncio
import backoff
import logging
from typing import Coroutine, Any
from abc import abstractmethod, ABC
from aiohttp.client import ClientResponse
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientHttpProxyError, ContentTypeError
from aiohttp import (
    web,  # noqa --- required to use aiohttp.web
    ClientOSError,
    TooManyRedirects,
    client_exceptions,
    ClientResponseError,
)

from realfans_api.utils.requests.fake_agent import generate_proxy, generate_fake_agent


class RetryException(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ExternalAPIException(Exception):
    pass


class ForbiddenException(Exception):
    pass


WINDOWS_OS = sys.platform == "win32"
AGENT_AUTO_RETRY = (ClientProxyConnectionError, ClientHttpProxyError, ForbiddenException)


def is_faulty_proxy_exception(exception: Exception):
    return type(exception) in AGENT_AUTO_RETRY


def is_random_server_errors(exception: Exception):
    return type(exception) in [TooManyRedirects]


def on_not_worth_retry_exception(exception: Exception):
    return is_faulty_proxy_exception(exception) or is_random_server_errors(exception)


class APIInterfaceAsync(ABC):
    ROOT_URL: str
    RETRY_ON_STR_IN_RESPONSE = []

    def __init__(self, proxy=None, raise_for_status=False):
        self.proxy = proxy
        self.session = None
        self.connector = None
        self.current_requests = 0
        self.max_proxy_requests = 0
        self.change_country = False
        self.raise_for_status = raise_for_status
        self.headers = self.__generate_fake_agent()

    @abstractmethod
    async def callback(self, response: ClientResponse):
        pass

    def change_agent(self):
        self.current_requests = 0
        self.proxy = self.__generate_proxy()
        self.headers = self.__generate_fake_agent()
        return self.proxy, self.headers

    async def __get_domain(self) -> str:
        return self.ROOT_URL

    async def request(
        self,
        endpoint: str,
        method: str,
        params={},
        headers={},
        data=None,
        json=None,
        url=None,
        callback=None,
        use_proxy=True,
    ) -> Any:  # sourcery skip: default-mutable-arg
        url = url or await self.__get_domain()
        final_url = url + endpoint if url else endpoint

        proxy = self.__update_agent()
        headers = self.__build_request_headers(headers)
        return await self.__request(
            final_url,
            method,
            headers,
            params,
            data,
            json,
            proxy=proxy if use_proxy else None,
            callback=callback,
        )

    def __generate_proxy(self):
        return generate_proxy(self.change_country)

    def __generate_fake_agent(self):
        return generate_fake_agent()

    def __build_request_headers(self, headers: dict) -> dict:
        headers = headers or {}
        if self.headers:
            headers.update(self.headers)
        return headers

    def __update_agent(self):
        if not self.proxy:
            return
        self.current_requests += 1
        if self.current_requests >= self.max_proxy_requests:
            self.change_agent()
        return self.proxy

    @backoff.on_exception(
        backoff.constant,
        (aiohttp.web.HTTPException, client_exceptions.ClientError, RetryException, ClientOSError),
        max_tries=2,
        interval=0,
        giveup=on_not_worth_retry_exception,
        backoff_log_level=logging.DEBUG,
        giveup_log_level=logging.DEBUG,
    )
    async def __request(self, *args, **kwargs):
        if kwargs.get("proxy"):
            print(f"Using proxy {kwargs.get('proxy')}")
            return await self.__proxy_request(*args, **kwargs)
        print("NOT USING PROXY")
        return await self.__session_request(*args, **kwargs)

    async def __session_request(
        self, url, method, headers=None, params=None, data=None, json=None, proxy=None, callback=None
    ):
        if not self.session:
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False, loop=asyncio.get_event_loop()),
                raise_for_status=self.raise_for_status,
            )
        else:
            self.session._cookie_jar.clear()
        async with self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
        ) as resp:
            return await self.__callback_or_raise_exception(resp, callback)

    async def __proxy_request(
        self, url, method, headers=None, params=None, data=None, json=None, proxy=None, callback=None
    ):
        max_tries = 2
        while max_tries:
            max_tries -= 1
            self.__setup_connector()
            try:
                async with aiohttp.ClientSession(
                    connector=self.connector,  # Needed for Ubuntu not to throttle
                    raise_for_status=self.raise_for_status,
                ) as client:
                    async with client.request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        json=json,
                        proxy=proxy,
                        headers=headers,
                    ) as resp:
                        return await self.__callback_or_raise_exception(resp, callback)
            except AGENT_AUTO_RETRY:
                if not max_tries:
                    raise
                proxy, headers = self.change_agent()

    def __setup_connector(self):
        if self.connector:
            self.connector._cleanup()
        self.connector = aiohttp.TCPConnector(
            ssl=False,
            loop=asyncio.get_event_loop(),
            force_close=WINDOWS_OS,
            keepalive_timeout=None if WINDOWS_OS else 0,
        )

    async def __callback_or_raise_exception(self, response: ClientResponse, callback: Coroutine):
        # sourcery skip: raise-from-previous-error
        if response.status == 403:
            raise ForbiddenException(await response.text())
        try:
            return await callback(response) if callback else await self.callback(response)
        except (RetryException, ExternalAPIException):
            raise
        except (ContentTypeError, ClientResponseError) as exc:
            # ClientResponseError => triggered when raise_for_status=True, happens when we have status codes in the 400s and 500s
            content = await response.text()
            raise ExternalAPIException(
                f"{self.__get_error_msg_from_exception(exc, response.url)} - Response:\n'{content}'"
            )
        except Exception as exc:
            raise ExternalAPIException(self.__get_error_msg_from_exception(exc, response.url)) from exc

    def __get_error_msg_from_exception(self, exception: Exception, url) -> str:
        # Replacing any instance of URL since it could have private data eg: Auth keys
        exception_error_msg = f"{type(exception)}: {exception}"
        exception_error_msg = exception_error_msg.replace(str(url), self.__class__.__name__)
        return exception_error_msg
