"""売買内訳データ (/markets/breakdown).

https://jpx.gitbook.io/j-quants-ja/api-reference/breakdown
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class BreakdownStream(JQuantsDateStream):
    """the breakdown stream."""

    name = "breakdown"
    path = "/markets/breakdown"
    primary_keys = ["date", "code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "breakdown.json"
    records_jsonpath = "$.breakdown[*]"
