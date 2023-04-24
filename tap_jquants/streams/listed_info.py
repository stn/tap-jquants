from typing import Dict

from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 上場銘柄一覧(/listed/info)
# https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info


class ListedInfo(IncrementalTableStream):
    """the listed info stream"""

    tap_stream_id = "listed_info"
    path = "listed/info"
    key_properties = [
        "code",
        "date",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 1
    bookmark_offset = 0

    data_key = "info"

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for listed_info."""
        code = self.config.get("code")
        return {
            "code": code,
            "date": start_date,
        }
