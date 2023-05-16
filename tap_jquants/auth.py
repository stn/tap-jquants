"""Authentication for tap-jquants."""

from __future__ import annotations

import typing as t

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator, SingletonMeta

from .exceptions import JQuantsError

if t.TYPE_CHECKING:
    from .client import JQuantsStream


class JQuantsAuthenticator(BearerTokenAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for J-Quants."""

    @classmethod
    def _get_refresh_token(
        cls: type[JQuantsAuthenticator],
        stream: JQuantsStream,
        session: requests.Session,
    ) -> str:
        """Get a refresh token."""
        response = session.post(
            url=f"{stream.url_base}/token/auth_user",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "mailaddress": stream.config["mail_address"],
                "password": stream.config["password"],
            },
        )
        if response.status_code != requests.codes.ok:
            raise JQuantsError(response)
        return response.json()["refreshToken"]

    @classmethod
    def _get_id_token(
        cls: type[JQuantsAuthenticator],
        stream: JQuantsStream,
        session: requests.Session,
    ) -> str:
        """Get an id token."""
        refresh_token = cls._get_refresh_token(stream, session)
        response = session.post(
            url=f"{stream.url_base}/token/auth_refresh?refreshtoken={refresh_token}",
            headers={
                "Content-Type": "application/json",
            },
        )
        if response.status_code != requests.codes.ok:
            raise JQuantsError(response)
        return response.json()["idToken"]

    @classmethod
    def create_for_stream(
        cls: type[JQuantsAuthenticator],
        stream: JQuantsStream,
    ) -> JQuantsAuthenticator:
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        with requests.Session() as session:
            id_token = cls._get_id_token(stream, session)
        return cls(
            stream=stream,
            token=id_token,
        )
