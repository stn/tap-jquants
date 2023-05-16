"""投資部門別情報 (/markets/trades_spec).

https://jpx.gitbook.io/j-quants-ja/api-reference/trades_spec
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsFromStream


class TradesSpecStream(JQuantsFromStream):
    """the trades_spec stream."""

    name = "trades_spec"
    path = "/markets/trades_spec"
    primary_keys = ["published_date", "section"]
    replication_key = "published_date"
    schema_filepath = SCHEMAS_DIR / "trades_spec.json"
    records_jsonpath = "$.trades_spec[*]"
