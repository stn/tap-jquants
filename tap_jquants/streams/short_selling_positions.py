"""空売り残高報告 (/markets/short_selling_positions).

https://jpx.gitbook.io/j-quants-ja/api-reference/short_selling_positions
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsFromStream


class ShortSellingPositionsStream(JQuantsFromStream):
    """the short_selling_positions stream."""

    name = "short_selling_positions"
    path = "/markets/short_selling_positions"
    primary_keys = ["disclosed_date", "code", "short_seller_name"]
    replication_key = "disclosed_date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "short_selling_positions.json"
    records_jsonpath = "$.short_selling_positions[*]"