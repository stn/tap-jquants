"""業種別空売り比率 (/markets/short_selling).

https://jpx.gitbook.io/j-quants-ja/api-reference/short_selling
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class ShortSellingStream(JQuantsDateStream):
    """the short_selling stream."""

    name = "short_selling"
    path = "/markets/short_selling"
    primary_keys = ["date", "sector33_code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "short_selling.json"
    records_jsonpath = "$.short_selling[*]"
