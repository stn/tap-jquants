from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 前場四本値(/prices/prices_am)
# https://jpx.gitbook.io/j-quants-ja/api-reference/prices_am
# パラメータにdateを持たないことに注意。


class PricesAm(IncrementalTableStream):
    """the prices_am stream"""

    tap_stream_id = "prices_am"
    path = "prices/prices_am"
    key_properties = [
        "date",
        "code",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 0

    data_key = "prices_am"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for prices_am."""
        code = self.config.get("code")
        return {
            "code": code,
        }
