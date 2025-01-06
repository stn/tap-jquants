"""財務情報 (/fins/statements).

https://jpx.gitbook.io/j-quants-ja/api-reference/statements
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class StatementsStream(JQuantsDateStream):
    """the statements stream."""

    name = "statements"
    path = "/fins/statements"
    primary_keys = ["disclosed_date", "local_code", "disclosure_number"]
    replication_key = "disclosed_date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "statements.json"
    records_jsonpath = "$.statements[*]"

    def post_process(
        self,
        row: dict,
        _context: dict | None = None,
    ) -> dict | None:
        if row["changes_other_than_ones_based_on_revisions_of_accounting_standard"]:
            row["changes_other_than_ones_based_on_revisions_of_accounting_standa"] = row["changes_other_than_ones_based_on_revisions_of_accounting_standard"]
            del row["changes_other_than_ones_based_on_revisions_of_accounting_standard"]
        if row["number_of_issued_and_outstanding_shares_at_the_end_of_fiscal_year_including_treasury_stock"]:
            row["number_of_issued_and_outstanding_shares_at_the_end_of_fiscal_ye"] = row["number_of_issued_and_outstanding_shares_at_the_end_of_fiscal_year_including_treasury_stock"]
            del row["number_of_issued_and_outstanding_shares_at_the_end_of_fiscal_year_including_treasury_stock"]
        if row["next_year_forecast_non_consolidated_earnings_per_share2nd_quarter"]:
            row["next_year_forecast_non_consolidated_earnings_per_share2nd_quart"] = row["next_year_forecast_non_consolidated_earnings_per_share2nd_quarter"]
            del row["next_year_forecast_non_consolidated_earnings_per_share2nd_quarter"]
        return row
