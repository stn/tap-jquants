"""決算発表予定日 (/fins/announcement).

https://jpx.gitbook.io/j-quants-ja/api-reference/announcement
"""

from tap_jquants.client import SCHEMAS_DIR, JQuantsStream


class AnnouncementStream(JQuantsStream):
    """the announcement stream."""

    name = "announcement"
    path = "/fins/announcement"
    primary_keys = ["date", "code"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "announcement.json"
    records_jsonpath = "$.announcement[*]"
