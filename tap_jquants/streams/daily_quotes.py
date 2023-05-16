"""株価四本値 (/prices/daily_quotes).

https://jpx.gitbook.io/j-quants-ja/api-reference/daily_quotes
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class DailyQuotesStream(JQuantsDateStream):
    """the daily_quotes stream."""

    name = "daily_quotes"
    path = "/prices/daily_quotes"
    primary_keys = ["date", "code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "daily_quotes.json"
    records_jsonpath = "$.daily_quotes[*]"
