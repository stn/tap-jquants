from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 業種別空売り比率(/markets/short_selling)
# https://jpx.gitbook.io/j-quants-ja/api-reference/short_selling


class ShortSelling(IncrementalTableStream):
    """the short_selling stream"""

    tap_stream_id = "short_selling"
    path = "markets/short_selling"
    key_properties = [
        "date",
        "sector33_code",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 1

    data_key = "short_selling"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for short_selling."""
        code = self.config.get("code")
        if code:
            return {
                "sector33code": code,
                "from": start_date,
            }
        return {
            "date": start_date,
        }
