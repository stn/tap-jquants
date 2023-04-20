from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# オプション四本値(/option/index_option)
# https://jpx.gitbook.io/j-quants-ja/api-reference/index_option


class IndexOption(IncrementalTableStream):
    """the index_option stream"""

    tap_stream_id = "index_option"
    path = "option/index_option"
    key_properties = [
        "date",
        "code",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 1

    data_key = "index_option"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for index_option."""
        return {
            "date": start_date,
        }
