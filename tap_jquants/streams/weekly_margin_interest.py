from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 信用取引週末残高(/markets/weekly_margin_interest)
# https://jpx.gitbook.io/j-quants-ja/api-reference/weekly_margin_interest


class WeeklyMarginInterest(IncrementalTableStream):
    """the weekly_margin_interest stream"""

    tap_stream_id = "weekly_margin_interest"
    path = "markets/weekly_margin_interest"
    key_properties = [
        "date",
        "code",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 7

    data_key = "weekly_margin_interest"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for weekly_margin_interest."""
        code = self.config.get("code")
        if code:
            return {
                "code": code,
                "from": start_date,
            }
        return {
            "date": start_date,
        }
