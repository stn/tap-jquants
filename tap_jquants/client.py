from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import urllib.parse

import requests
import singer
from singer import metrics, utils

from .exceptions import raise_for_error


BASE_URL = "https://api.jquants.com/v1"
LOGGER = singer.get_logger()

# set default timeout of 300 seconds
REQUEST_TIMEOUT = 300


class JquantsClient:
    def __init__(self,
                 mail_address=None,
                 password=None,
                 timeout=REQUEST_TIMEOUT,
                 ):
        self._mail_address = mail_address
        self._password = password
        self._refresh_token = None
        self._refresh_token_expires = None
        self._id_token = None
        self._id_token_expires = None
        self._session = requests.Session()
        try:
            self.request_timeout = REQUEST_TIMEOUT if timeout in (None, 0, "0", "0.0") else float(timeout)
        except ValueError:
            self.request_timeout = REQUEST_TIMEOUT

    def __enter__(self):
        self.get_id_token()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def get_id_token(self) -> None:
        """Get an id token"""
        if self._id_token and self._id_token_expires > datetime.now(timezone.utc):
            return

        self.get_refresh_token()
        response = self._session.post(
            url=f"{BASE_URL}/token/auth_refresh?refreshtoken={self._refresh_token}",
            headers={
                "Content-Type": "application/json",
            },
            timeout=self.request_timeout,
        )

        if response.status_code != 200:
            raise_for_error(response)

        data = response.json()
        self._id_token = data["idToken"]
        self._id_token_expires = utils.now() + timedelta(hours=24)

        LOGGER.info("Get the id token, token expires = %s", self._id_token_expires)

    def get_refresh_token(self) -> None:
        """Get a refresh token"""
        if self._refresh_token and self._refresh_token_expires > datetime.now(timezone.utc):
            return

        response = self._session.post(
            url=f"{BASE_URL}/token/auth_user",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "mailaddress": self._mail_address,
                "password": self._password,
            },
            timeout=self.request_timeout,
        )
        LOGGER.debug(response)

        if response.status_code != 200:
            raise_for_error(response)

        data = response.json()
        self._refresh_token = data["refreshToken"]
        self._refresh_token_expires = utils.now() + timedelta(weeks=1)

        LOGGER.info("Get a refresh token, token expires = %s", self._refresh_token_expires)

    @utils.ratelimit(12, 60)
    def request(self, method: str, path: str = None, params: Dict = None, **kwargs) -> Any:
        """Wrapper method around request.sessions get/post method using
        the session object of JquantsClient object."""

        self.get_id_token()

        if params:
            params = {k: v for k, v in params.items() if v is not None}
        url = f"{BASE_URL}/{path}?{urllib.parse.urlencode(params)}" if params else f"{BASE_URL}/{path}"

        endpoint = kwargs.pop("endpoint", None)
        kwargs["headers"] = kwargs.get("headers", {})
        kwargs["headers"]["Authorization"] = f"Bearer {self._id_token}"
        if method == "POST":
            kwargs["headers"]["Content-Type"] = "application/json"

        with metrics.http_request_timer(endpoint) as timer:
            response = self._session.request(method, url, timeout=self.request_timeout, **kwargs)
            timer.tags[metrics.Tag.http_status_code] = response.status_code

        if response.status_code != 200:
            raise_for_error(response)

        response.encoding = "utf-8"
        return response.json()

    def get(self, path: str, params: Dict = None, **kwargs) -> Any:
        """wrapper for get method."""
        return self.request("GET", path=path, params=params, **kwargs)

    def post(self, path: str, params: Dict = None, **kwargs) -> Any:
        """wrapper for post method."""
        return self.request("POST", path=path, params=params, **kwargs)
