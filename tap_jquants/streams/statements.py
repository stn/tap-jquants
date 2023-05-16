"""財務情報 (/fins/statements).

https://jpx.gitbook.io/j-quants-ja/api-reference/statements
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class StatementsStream(JQuantsDateStream):
    """the statements stream."""

    name = "statements"
    path = "/fins/statements"
    primary_keys = ["disclosed_date", "local_code"]
    replication_key = "disclosed_date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "statements.json"
    records_jsonpath = "$.statements[*]"
