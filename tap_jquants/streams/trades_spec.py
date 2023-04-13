from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 投資部門別情報(/markets/trades_spec)
# https://jpx.gitbook.io/j-quants-ja/api-reference/trades_spec


class TradesSpec(IncrementalTableStream):
    """the trades_spec stream"""

    tap_stream_id = "trades_spec"
    path = "markets/trades_spec"
    key_properties = [
        "published_date",
        "section",
    ]
    valid_replication_keys = ["published_date"]
    date_window_size = 1

    data_key = "trades_spec"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for trades_spec."""
        section = self.config.get("section")
        return {
            "section": section,
            "from": start_date,
            "to": end_date,
        }
