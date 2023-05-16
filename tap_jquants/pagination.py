"""Generic paginator classes."""

from __future__ import annotations

import re
import typing as t

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator

if t.TYPE_CHECKING:
    from requests import Response

from .helpers import get_next_date

T = t.TypeVar("T")
TPageToken = t.TypeVar("TPageToken")

PAGINATOR_JSONPATH = "$.pagination_key[*]"
DATE_PAT = re.compile(r"date=(\d{4}-\d{2}-\d{2})")


class JQuantsDatePaginator(BaseAPIPaginator[t.Optional[t.Tuple[str, str]]]):
    """Paginator class for APIs returning a pagination token in the response body."""

    def __init__(
        self,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
        """Create a new paginator.

        Args:
            args: Paginator positional arguments for base class.
            kwargs: Paginator keyword arguments for base class.
        """
        super().__init__(None, *args, **kwargs)

    def get_next(self, response: Response) -> tuple[str, str | None] | None:
        """Get the next page token.

        Args:
            response: API response object.

        Returns:
            The next page token.
        """
        date_key = re.search(  # type: ignore[union-attr]
            DATE_PAT,
            response.request.url,  # type: ignore[arg-type]
        ).group(
            1,
        )
        pagination_key = next(
            extract_jsonpath(PAGINATOR_JSONPATH, response.json()),
            None,
        )
        if pagination_key is not None:
            return date_key, pagination_key
        date_key = get_next_date(date_key)
        if date_key is None:
            return None
        return date_key, None
