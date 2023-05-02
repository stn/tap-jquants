from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 配当金情報(/fins/dividend)
# https://jpx.gitbook.io/j-quants-ja/api-reference/dividend


class FinsDividend(IncrementalTableStream):
    """the fins_dividend stream"""

    tap_stream_id = "fins_dividend"
    path = "fins/dividend"
    key_properties = ["reference_number"]
    replication_key = "announcement_date"
    valid_replication_keys = ["announcement_date"]
    date_window_size = 1

    data_key = "dividend"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for fins_dividend."""
        code = self.config.get("code")
        if code:
            return {
                "code": code,
                "from": start_date,
            }
        return {
            "date": start_date,
        }
