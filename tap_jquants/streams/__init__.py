"""Stream classes for tap-jquants."""

from tap_jquants.streams.announcement import AnnouncementStream
from tap_jquants.streams.breakdown import BreakdownStream
from tap_jquants.streams.daily_quotes import DailyQuotesStream
from tap_jquants.streams.dividend import DividendStream
from tap_jquants.streams.fs_details import FsDetailsStream
from tap_jquants.streams.index_option import IndexOptionStream
from tap_jquants.streams.indices import IndicesStream
from tap_jquants.streams.listed_info import ListedInfoStream
from tap_jquants.streams.prices_am import PricesAmStream
from tap_jquants.streams.short_selling import ShortSellingStream
from tap_jquants.streams.short_selling_positions import ShortSellingPositionsStream
from tap_jquants.streams.statements import StatementsStream
from tap_jquants.streams.topix import TopixStream
from tap_jquants.streams.trades_spec import TradesSpecStream
from tap_jquants.streams.trading_calendar import TradingCalendarStream
from tap_jquants.streams.weekly_margin_interest import WeeklyMarginInterestStream

__all__ = [
    "AnnouncementStream",
    "BreakdownStream",
    "DailyQuotesStream",
    "DividendStream",
    "FsDetailsStream",
    "IndexOptionStream",
    "IndicesStream",
    "TopixStream",
    "ListedInfoStream",
    "PricesAmStream",
    "ShortSellingStream",
    "ShortSellingPositionsStream",
    "StatementsStream",
    "TradesSpecStream",
    "TradingCalendarStream",
    "WeeklyMarginInterestStream",
]
