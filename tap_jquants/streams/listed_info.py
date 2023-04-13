from typing import Dict, Iterator

from singer.logger import get_logger

from ..helpers import convert_json
from .abstract import FullTableStream

LOGGER = get_logger()

# 上場銘柄一覧(/listed/info)
# https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info


class ListedInfo(FullTableStream):
    """the listed info stream"""

    tap_stream_id = "listed_info"
    path = "listed/info"
    key_properties = [
        "code",
        "date",
    ]

    data_key = "info"

    def get_records(self) -> Iterator[Dict]:
        """Performs API calls to extract data for each site."""
        # 過去日付の指定について、Premiumプランでデータ提供開始日（2008年5月7日）より過去日付を指定した場合であっても、2008年5月7日時点の銘柄情報を返却します。
        # また、指定された日付が休業日の場合は指定日の翌営業日の銘柄情報を返却します。
        params = {
            "date": self.config.get("date"),
        }
        data = self.client.get(self.path, params)
        # transforms data by converting camelCase fields to snake_case fields
        transformed_records = convert_json(data)
        yield from transformed_records.get(self.data_key, [])
