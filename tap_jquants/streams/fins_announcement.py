from singer.logger import get_logger

from .abstract import IncrementalTableStream

LOGGER = get_logger()

# 決算発表予定日(/fins/announcement)
# https://jpx.gitbook.io/j-quants-ja/api-reference/announcement


class FinsAnnouncement(IncrementalTableStream):
    """the fins_announcement stream"""

    tap_stream_id = "fins_announcement"
    path = "fins/announcement"
    key_properties = [
        "code",
        "date",
    ]
    valid_replication_keys = ["date"]
    date_window_size = 0

    data_key = "announcement"
