"""REST client handling, including JQuantsStream base class."""

from __future__ import annotations

import sys
import typing as t
from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_jquants.auth import JQuantsAuthenticator
from tap_jquants.pagination import JQuantsDatePaginator

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

from .helpers import convert_json

if t.TYPE_CHECKING:
    from singer_sdk.pagination import BaseAPIPaginator


_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class JQuantsStream(RESTStream):
    """JQuants stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.jquants.com/v1"

    next_page_token_jsonpath = "$.pagination_key"  # noqa: S105

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return JQuantsAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_url_params(
        self,
        _context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["pagination_key"] = next_page_token
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=convert_json(response.json()),
        )


class JQuantsDateStream(JQuantsStream):
    """JQuants incremental stream class based on date."""

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Return a new paginator object."""
        return JQuantsDatePaginator()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of parameters to use in the URL."""
        params: dict = {}
        if next_page_token is not None:
            date_key, pagination_key = next_page_token
            if pagination_key:
                params["pagination_key"] = next_page_token
            params["date"] = date_key
        else:
            starting_date = self.get_starting_timestamp(context)
            if starting_date:
                params["date"] = starting_date.strftime("%Y-%m-%d")
        self.logger.info("URL params: %s", params)
        return params


class JQuantsFromStream(JQuantsStream):
    """JQuants incremental stream class based on from."""

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of parameters to use in the URL."""
        params: dict = {}
        if next_page_token is not None:
            pagination_key = next_page_token
            if pagination_key:
                params["pagination_key"] = next_page_token
        starting_date = self.get_starting_timestamp(context)
        if starting_date:
            params["from"] = starting_date.strftime("%Y-%m-%d")
        self.logger.info("URL params: %s", params)
        return params
