"""前場四本値 (/prices/prices_am).

https://jpx.gitbook.io/j-quants-ja/api-reference/prices_am
"""

from tap_jquants.client import SCHEMAS_DIR, JQuantsStream


class PricesAmStream(JQuantsStream):
    """the prices_am stream."""

    name = "prices_am"
    path = "/prices/prices_am"
    primary_keys = ["date", "code"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "prices_am.json"
    records_jsonpath = "$.prices_am[*]"
