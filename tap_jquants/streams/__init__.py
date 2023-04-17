from typing import Mapping, Type

from .abstract import BaseStream
from .daily_quotes import DailyQuotes
from .fins_statements import FinsStatements
from .indices_topix import IndicesTopix
from .listed_info import ListedInfo
from .trades_spec import TradesSpec

STREAMS: Mapping[str, Type[BaseStream]] = {
    DailyQuotes.tap_stream_id: DailyQuotes,
    FinsStatements.tap_stream_id: FinsStatements,
    IndicesTopix.tap_stream_id: IndicesTopix,
    ListedInfo.tap_stream_id: ListedInfo,
    TradesSpec.tap_stream_id: TradesSpec,
}
