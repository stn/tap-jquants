"""財務諸表(BS/PL) (/fins/fs_details).

https://jpx.gitbook.io/j-quants-ja/api-reference/statements-1
"""

from __future__ import annotations

from tap_jquants.client import SCHEMAS_DIR, JQuantsDateStream


class FsDetailsStream(JQuantsDateStream):
    """the statement details stream."""

    name = "fs_details"
    path = "/fins/fs_details"
    primary_keys = ["disclosed_date", "local_code"]
    replication_key = "disclosed_date"
    is_sorted = True
    schema_filepath = SCHEMAS_DIR / "fs_details.json"
    records_jsonpath = "$.fs_details[*]"
