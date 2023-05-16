"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_jquants.tap import TapJQuants

SAMPLE_CONFIG = {
    "mail_address": "foobar@example.com",
    "password": "abc123",
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
}


# Run standard built-in tap tests from the SDK:
TestTapJQuants = get_tap_test_class(
    tap_class=TapJQuants,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
