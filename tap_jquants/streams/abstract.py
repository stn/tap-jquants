from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Iterator, List, Optional, Tuple

from singer import Transformer, metrics, utils, write_record, write_state
from singer.logger import get_logger
from singer.metadata import get_standard_metadata

from ..helpers import convert_json

PAGINATION_KEY = "pagination_key"
LOGGER = get_logger()


class BaseStream(ABC):
    """Base class representing generic stream methods and meta-attributes."""

    @property
    @abstractmethod
    def replication_method(self) -> str:
        """Defines the sync mode of a stream."""

    @property
    @abstractmethod
    def replication_key(self) -> Optional[str]:
        """Defines the replication key for incremental sync mode of a stream."""

    @property
    @abstractmethod
    def valid_replication_keys(self) -> Optional[List[str]]:
        """Defines the replication key for incremental sync mode of a stream."""

    @property
    @abstractmethod
    def key_properties(self) -> List[str]:
        """List of key properties for stream."""

    @property
    @abstractmethod
    def tap_stream_id(self) -> str:
        """The unique identifier for the stream.

        This is allowed to be different from the name of the stream in
        order to allow for sources that have duplicate stream names.
        """

    @property
    @abstractmethod
    def path(self) -> str:
        """Defines the path of a stream."""

    @property
    @abstractmethod
    def data_key(self) -> str:
        """The data key of a response."""

    @abstractmethod
    def sync(self, state: Dict, schema: Dict, stream_metadata: Dict):
        """Performs Sync."""

    def __init__(self, client=None, config=None) -> None:
        self.client = client
        self.config = config

    @classmethod
    def get_metadata(cls, schema) -> Dict[str, str]:
        """Returns a `dict` for generating stream metadata."""
        return get_standard_metadata(
            **{
                "schema": schema,
                "key_properties": cls.key_properties,
                "valid_replication_keys": cls.valid_replication_keys,
                "replication_method": cls.replication_method,
            }
        )


class IncrementalTableStream(BaseStream, ABC):
    """Base Class for Incremental Stream."""

    replication_method = "INCREMENTAL"
    replication_key = "date"
    now_dt_tm = utils.now()

    # declaring this variable to keep track of number of
    # records processed per stream, per site, per sub_type
    records_extracted = 0

    @staticmethod
    def get_bookmark(state: Dict, stream: str, default=None) -> str:
        """Fetches the bookmark from the state file for a given stream."""
        if (state is None) or ("bookmarks" not in state):
            return default
        return state.get("bookmarks", {}).get(stream, default)

    @property
    def date_window_size(self) -> int:
        """The number of days to request data.
        The default is 1. If it is 0, end_dt is set to today."""
        return 1

    @property
    def bookmark_offset(self) -> int:
        """The number of days to proceed data against bookmark.
        The default is 1."""
        return 1

    @property
    def skip_non_business_day(self) -> bool:
        """The flag to skip non-business days.
        The default is False."""
        return False

    def write_bookmark(self, state: Dict, value: str) -> None:
        """Writes bookmark to state file for a given stream."""
        if "bookmarks" not in state:
            state["bookmarks"] = {}
        state["bookmarks"][self.tap_stream_id] = value
        LOGGER.info(f"Write state for Stream: {self.tap_stream_id}, value: {value}")
        write_state(state)

    def get_start_and_end_times(self, state: Dict, stream: str) -> Tuple[datetime, datetime]:
        """Gets start and end times."""
        # get the bookmark from state file
        report_bookmark = self.get_bookmark(state, stream)
        if report_bookmark:
            start_dt_tm = utils.strptime_to_utc(report_bookmark) + timedelta(days=self.bookmark_offset)
            start_dt_tm = self.get_start_dt_tm_in_business(start_dt_tm)
        else:
            start_dt_tm = utils.strptime_to_utc(self.config.get("start_date"))

        if self.date_window_size > 0:
            end_dt_tm = start_dt_tm + timedelta(days=self.date_window_size)
            if end_dt_tm > self.now_dt_tm:
                end_dt_tm = self.now_dt_tm + timedelta(days=1)
        else:
            end_dt_tm = self.now_dt_tm + timedelta(days=1)

        return start_dt_tm, end_dt_tm

    def proceed_start_end_dt_tm(self, end_dt_tm: datetime) -> Tuple[datetime, datetime]:
        """Gets start_date_time of a new window to end_date_time of old window
        Sets end_date_time of new window to date_window_size days ahead
        since start_date_time."""
        start_dt_tm = end_dt_tm
        start_dt_tm = self.get_start_dt_tm_in_business(start_dt_tm)
        if self.date_window_size > 0:
            end_dt_tm = start_dt_tm + timedelta(days=self.date_window_size)
            if end_dt_tm > self.now_dt_tm:
                end_dt_tm = self.now_dt_tm + timedelta(days=1)
        else:
            end_dt_tm = self.now_dt_tm + timedelta(days=1)

        return start_dt_tm, end_dt_tm

    def get_start_dt_tm_in_business(self, start_dt_tm) -> datetime:
        """Gets start_dt_tm in business day if skip_holiday is True."""
        if self.skip_non_business_day:
            if start_dt_tm.month == 1 and start_dt_tm.day <= 3:
                return start_dt_tm + timedelta(days=4 - start_dt_tm.day)
            elif start_dt_tm.month == 12 and start_dt_tm.day == 31:
                return start_dt_tm + timedelta(days=4)
            elif start_dt_tm.weekday() == 5:
                return start_dt_tm + timedelta(days=2)
            elif start_dt_tm.weekday() == 6:
                return start_dt_tm + timedelta(days=1)
        return start_dt_tm

    def make_payload(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates payload for POST API Call.
        The default implementation returns an empty."""
        return {}

    def make_params(self, start_date: str, end_date: str, stream_metadata: Dict) -> Dict:
        """Creates params for API Call.
        The default implementation returns an empty."""
        return {}

    def validate_keys_in_data(self, extracted_data: List) -> None:
        """Validates the data by checking the primary keys in extracted data."""
        for record in extracted_data:
            for key in self.key_properties:
                if not record.get(key):
                    primary_keys_only = {id_field: record.get(id_field) for id_field in self.key_properties}
                    raise ValueError(f"Missing key {key} in record with primary keys {primary_keys_only}")

    def process_records(
        self,
        schema: Dict,
        stream_metadata: Dict,
        records: List,
        time_extracted: datetime,
    ) -> Optional[str]:
        """Filters out the unselected fields by the user Picks the latest
        bookmark value from extracted data Writes the records to stdout."""
        max_bookmark_dt_tm = None
        with metrics.record_counter(self.tap_stream_id) as counter:
            for record in records:
                # Transform record for Singer.io
                with Transformer() as transformer:
                    transformed_record = transformer.transform(record, schema, stream_metadata)

                    # Reset max_bookmark_value to new value if higher
                    if self.replication_key in transformed_record:  # replication_keyが日付ではないケースは考慮していない
                        bookmark_date = transformed_record.get(self.replication_key)
                        bookmark_dt_tm = utils.strptime_to_utc(bookmark_date)
                        if max_bookmark_dt_tm:
                            if bookmark_dt_tm > max_bookmark_dt_tm:
                                max_bookmark_dt_tm = bookmark_dt_tm
                        else:
                            max_bookmark_dt_tm = bookmark_dt_tm
                        write_record(self.tap_stream_id, transformed_record, time_extracted=time_extracted)
                        counter.increment()
                    else:
                        write_record(self.tap_stream_id, transformed_record, time_extracted=time_extracted)
                        counter.increment()

            LOGGER.info(f"Stream: {self.tap_stream_id}, Processed {counter.value} records")
            self.records_extracted += counter.value
            if max_bookmark_dt_tm:
                return utils.strftime(max_bookmark_dt_tm)
            return None

    def get_records(self, state: Dict, schema: Dict, stream_metadata: Dict) -> None:
        """Sync the data for a given stream.
        Gets the bookmark value or start date value, extracts data."""
        start_dt_tm, end_dt_tm = self.get_start_and_end_times(state, self.tap_stream_id)
        LOGGER.info(f"bookmark value or start date for {self.tap_stream_id}: {start_dt_tm}")
        while start_dt_tm < end_dt_tm:
            start_str, end_str = utils.strftime(start_dt_tm)[:10], utils.strftime(end_dt_tm)[:10]

            LOGGER.info(f"Running sync for {self.tap_stream_id} between date window {start_str} {end_str}")
            payload = self.make_payload(start_str, end_str, stream_metadata)
            params = self.make_params(start_str, end_str, stream_metadata)
            time_extracted = utils.now()
            LOGGER.info(f"params = {params}, payload = {payload}")
            data = self.client.get(self.path, endpoint=self.tap_stream_id, params=params, json=payload)
            if not data:
                LOGGER.info(f"There are no raw data records for date window {start_dt_tm} to {end_dt_tm}")
                start_dt_tm, end_dt_tm = self.proceed_start_end_dt_tm(end_dt_tm)
                continue

            transformed_data = []
            if self.data_key in data:
                transformed_data = convert_json(data)[self.data_key]

            while PAGINATION_KEY in data:
                pagination_key = data[PAGINATION_KEY]
                LOGGER.info(f"continuing pagination len(data)={len(transformed_data)}")
                params[PAGINATION_KEY] = pagination_key
                data = self.client.get(self.path, endpoint=self.tap_stream_id, params=params, json=payload)
                if self.data_key in data:
                    transformed_data.extend(convert_json(data)[self.data_key])

            if not transformed_data:
                start_dt_tm, end_dt_tm = self.proceed_start_end_dt_tm(end_dt_tm)
                continue

            self.validate_keys_in_data(transformed_data)
            LOGGER.info(f"Total synced records for {self.tap_stream_id}: {len(transformed_data)}")
            bookmark_value = self.process_records(
                schema,
                stream_metadata,
                transformed_data,
                time_extracted,
            )
            if bookmark_value:
                self.write_bookmark(state, bookmark_value)

            start_dt_tm, end_dt_tm = self.proceed_start_end_dt_tm(end_dt_tm)

    def sync(self, state: Dict, schema: Dict, stream_metadata: Dict) -> None:
        """Starts Sync."""
        LOGGER.info(f"Starting Sync for Stream {self.tap_stream_id}")
        self.records_extracted = 0
        self.get_records(state, schema, stream_metadata)
        LOGGER.info(f"Total records extracted for Stream: {self.tap_stream_id}: {self.records_extracted}")
        LOGGER.info(f"Finished Sync for Stream {self.tap_stream_id}")


class FullTableStream(BaseStream, ABC):
    """Base Class for full table Stream."""

    replication_method = "FULL_TABLE"
    api_method = "GET"
    valid_replication_keys = None
    replication_key = None

    def make_params(self) -> Dict:
        """Creates params for API Call.
        The default implementation returns an empty."""
        return {}

    def get_records(self) -> Iterator[Dict]:
        """Performs API calls to extract data for each site."""
        params = self.make_params()
        LOGGER.info(f"params = {params}")
        data = self.client.get(self.path, params)
        # transforms data by converting camelCase fields to snake_case fields
        transformed_records = convert_json(data)
        yield from transformed_records.get(self.data_key, [])

    def sync(self, state: Dict, schema: Dict, stream_metadata: Dict):
        LOGGER.info("sync called from %s", self.__class__)
        with metrics.record_counter(self.tap_stream_id) as counter:
            time_extracted = utils.now()
            for record in self.get_records():
                with Transformer() as transformer:
                    transformed_record = transformer.transform(record, schema, stream_metadata)
                    write_record(self.tap_stream_id, transformed_record, time_extracted=time_extracted)
                    counter.increment()
