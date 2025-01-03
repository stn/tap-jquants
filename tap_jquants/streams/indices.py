"""指数四本値 (/indices).

https://jpx.gitbook.io/j-quants-ja/api-reference/indicies
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class IndicesStream(JQuantsDateStream):
    """the indices stream."""

    name = "indices"
    path = "/indices"
    primary_keys = ["date", "code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "indices.json"
    records_jsonpath = "$.indices[*]"
