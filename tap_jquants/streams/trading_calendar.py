"""取引カレンダー (/markets/trading_calendar).

https://jpx.gitbook.io/j-quants-ja/api-reference/trading_calendar
"""

from __future__ import annotations

from typing import Any

from tap_jquants.client import SCHEMAS_DIR, JQuantsStream


class TradingCalendarStream(JQuantsStream):
    """the trading_calendar stream."""

    name = "trading_calendar"
    path = "/markets/trading_calendar"
    primary_keys = ["date"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "trading_calendar.json"
    records_jsonpath = "$.trading_calendar[*]"

    def get_url_params(
        self,
        context: dict | None,
        _next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of parameters to use in the URL."""
        params: dict = {}
        starting_date = self.get_starting_timestamp(context)
        if starting_date:
            params["from"] = starting_date.strftime("%Y-%m-%d")
        return params
