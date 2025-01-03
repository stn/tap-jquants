"""JQuants tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_jquants import streams


class TapJQuants(Tap):
    """JQuants tap class."""

    name = "tap-jquants"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "mail_address",
            th.StringType,
            required=True,
            description="The mail address to authenticate against J-Quants API",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="The password to authenticate against J-Quants API",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.JQuantsStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.AnnouncementStream(self),
            streams.BreakdownStream(self),
            streams.DailyQuotesStream(self),
            streams.DividendStream(self),
            streams.FsDetailsStream(self),
            streams.IndexOptionStream(self),
            streams.IndicesStream(self),
            streams.TopixStream(self),
            streams.ListedInfoStream(self),
            streams.PricesAmStream(self),
            streams.ShortSellingStream(self),
            streams.StatementsStream(self),
            streams.TradesSpecStream(self),
            streams.TradingCalendarStream(self),
            streams.WeeklyMarginInterestStream(self),
        ]


if __name__ == "__main__":
    TapJQuants.cli()
