"""オプション四本値 (/option/index_option).

https://jpx.gitbook.io/j-quants-ja/api-reference/index_option
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class IndexOptionStream(JQuantsDateStream):
    """the index_option stream."""

    name = "index_option"
    path = "/option/index_option"
    primary_keys = ["date", "code"]
    replication_key = "date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "index_option.json"
    records_jsonpath = "$.index_option[*]"

    def post_process(
        self,
        row: dict,
        _context: dict | None = None,
    ) -> dict | None:
        """Fix empty string in some night session data to None."""
        if not row["night_session_open"]:
            row["night_session_open"] = None
            row["night_session_high"] = None
            row["night_session_low"] = None
            row["night_session_close"] = None
        if not row["volume_only_auction"]:
            row["volume_only_auction"] = None
        if not row["last_trading_day"]:
            row["last_trading_day"] = None
        if not row["special_quotation_day"]:
            row["special_quotation_day"] = None
        if not row["settlement_price"]:
            row["settlement_price"] = None
        if not row["theoretical_price"]:
            row["theoretical_price"] = None
        if not row["base_volatility"]:
            row["base_volatility"] = None
        if not row["underlying_price"]:
            row["underlying_price"] = None
        if not row["implied_volatility"]:
            row["implied_volatility"] = None
        if not row["interest_rate"]:
            row["interest_rate"] = None
        return row
