from typing import Mapping, Type

from .abstract import BaseStream
from .daily_quotes import DailyQuotes
from .fins_announcement import FinsAnnouncement
from .fins_statements import FinsStatements
from .index_option import IndexOption
from .indices_topix import IndicesTopix
from .listed_info import ListedInfo
from .short_selling import ShortSelling
from .trades_spec import TradesSpec
from .weekly_margin_interest import WeeklyMarginInterest

STREAMS: Mapping[str, Type[BaseStream]] = {
    DailyQuotes.tap_stream_id: DailyQuotes,
    FinsAnnouncement.tap_stream_id: FinsAnnouncement,
    FinsStatements.tap_stream_id: FinsStatements,
    IndexOption.tap_stream_id: IndexOption,
    IndicesTopix.tap_stream_id: IndicesTopix,
    ListedInfo.tap_stream_id: ListedInfo,
    ShortSelling.tap_stream_id: ShortSelling,
    TradesSpec.tap_stream_id: TradesSpec,
    WeeklyMarginInterest.tap_stream_id: WeeklyMarginInterest,
}
