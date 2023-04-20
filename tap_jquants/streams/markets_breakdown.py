from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 売買内訳データ(/markets/breakdown)
# https://jpx.gitbook.io/j-quants-ja/api-reference/breakdown


class MarketsBreakdown(IncrementalTableStream):
    """the markets_breakdown stream"""

    tap_stream_id = "markets_breakdown"
    path = "markets/breakdown"
    key_properties = [
        "date",
        "code",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 1

    data_key = "breakdown"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for markets_breakdown."""
        code = self.config.get("code")
        if code:
            return {
                "code": code,
                "from": start_date,
            }
        return {
            "date": start_date,
        }
