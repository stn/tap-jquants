"""上場銘柄一覧 (/listed/info).

https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class ListedInfoStream(JQuantsDateStream):
    """the listed_info stream."""

    name = "listed_info"
    path = "/listed/info"
    primary_keys = ["date", "code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "listed_info.json"
    records_jsonpath = "$.info[*]"
