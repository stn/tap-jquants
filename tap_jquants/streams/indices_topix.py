from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# TOPIX指数四本値(/indices/topix)
# https://jpx.gitbook.io/j-quants-ja/api-reference/topix


class IndicesTopix(IncrementalTableStream):
    """the indices_topix stream"""

    tap_stream_id = "indices_topix"
    path = "indices/topix"
    key_properties = [
        "date",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 0

    data_key = "topix"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for API Call."""
        return {
            "from": start_date,
        }
