"""TOPIX指数四本値 (/indices/topix).

https://jpx.gitbook.io/j-quants-ja/api-reference/topix
"""

from tap_jquants.client import SCHEMAS_DIR, JQuantsStream


class TopixStream(JQuantsStream):
    """the topix stream."""

    name = "topix"
    path = "/indices/topix"
    primary_keys = ["date"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "topix.json"
    records_jsonpath = "$.topix[*]"
