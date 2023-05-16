"""配当金情報 (/fins/dividend).

https://jpx.gitbook.io/j-quants-ja/api-reference/dividend
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class DividendStream(JQuantsDateStream):
    """the dividend stream."""

    name = "dividend"
    path = "/fins/dividend"
    primary_keys = ["announcement_date", "announcement_time", "code"]
    replication_key = "announcement_date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "dividend.json"
    records_jsonpath = "$.dividend[*]"

    def post_process(
        self,
        row: dict,
        _context: dict | None = None,
    ) -> dict | None:
        """Converts number or string properties."""
        for key in [
            "gross_dividend_rate",
            "distribution_amount",
            "retained_earnings",
            "deemed_dividend",
            "deemed_capital_gains",
            "net_asset_decrease_ratio",
            "commemorative_dividend_rate",
            "special_dividend_rate",
        ]:
            num_key = f"{key}_num"
            if key not in row:
                continue
            value = row[key]
            if isinstance(value, str):
                if value and value != "-":
                    row[num_key] = float(value)
            else:
                row[key] = str(value)
                row[num_key] = value
        return row
