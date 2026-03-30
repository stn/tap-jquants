"""日々公表信用取引残高 (/markets/daily_margin_interest).

https://jpx.gitbook.io/j-quants-ja/api-reference/daily_margin_interest
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class DailyMarginInterestStream(JQuantsDateStream):
    """the daily_margin_interest stream."""

    name = "daily_margin_interest"
    path = "/markets/daily_margin_interest"
    primary_keys = ["published_date", "code"]
    replication_key = "published_date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "daily_margin_interest.json"
    records_jsonpath = "$.daily_margin_interest[*]"
