from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 株価四本値(/prices/daily_quotes)
# https://jpx.gitbook.io/j-quants-ja/api-reference/daily_quotes


class DailyQuotes(IncrementalTableStream):
    """the daily_quotes stream"""

    tap_stream_id = "daily_quotes"
    path = "prices/daily_quotes"
    key_properties = [
        "date",
        "code",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 1

    data_key = "daily_quotes"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for daily_quotes."""
        code = self.config.get("code")
        if code:
            return {
                "code": code,
                "from": start_date,
            }
        return {
            "date": start_date,
        }
