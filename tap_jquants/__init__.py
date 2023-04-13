#!/usr/bin/env python3
import os
import json
import singer
from singer import utils
from singer.schema import Schema

from .client import JquantsClient
from .discover import discover
from .sync import sync


REQUIRED_CONFIG_KEYS = ["mail_address", "password"]
LOGGER = singer.get_logger()


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        with JquantsClient(
            mail_address=args.config["mail_address"],
            password=args.config["password"],
        ) as client:
            catalog = args.catalog or discover()
            sync(client, args.config, args.state, catalog)


if __name__ == "__main__":
    main()
