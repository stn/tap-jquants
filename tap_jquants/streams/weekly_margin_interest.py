"""信用取引週末残高 (/markets/weekly_margin_interest).

https://jpx.gitbook.io/j-quants-ja/api-reference/weekly_margin_interest
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class WeeklyMarginInterestStream(JQuantsDateStream):
    """the weekly_margin_interest stream."""

    name = "weekly_margin_interest"
    path = "/markets/weekly_margin_interest"
    primary_keys = ["date", "code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "weekly_margin_interest.json"
    records_jsonpath = "$.weekly_margin_interest[*]"
