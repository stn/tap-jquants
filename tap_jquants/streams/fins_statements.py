from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 財務情報(/fins/statements)
# https://jpx.gitbook.io/j-quants-ja/api-reference/statements


class FinsStatements(IncrementalTableStream):
    """the fins_statements stream"""

    tap_stream_id = "fins_statements"
    path = "fins/statements"
    key_properties = [
        "disclosure_number",
    ]
    replication_key = "disclosed_date"
    valid_replication_keys = ["disclosed_date"]
    date_window_size = 1
    bookmark_offset = 0

    data_key = "statements"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for fins_statements."""
        code = self.config.get("code")
        return {
            "code": code,
            "date": start_date,
        }
