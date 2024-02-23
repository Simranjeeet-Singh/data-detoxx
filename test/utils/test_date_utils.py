import pytest
from datetime import datetime

from utils.date_utils import (
    convert_datetime_to_utc,
    convert_utc_to_sql_timestamp,
    convert_sql_timestamp_to_utc,
)


def test_convert_timestamp_to_utc_outputs_string_in_UTC_format_from_datetime_str():
    input = "2024-01-01 00:00:00.000"
    expout = "2024-01-01T000000000Z"
    assert convert_sql_timestamp_to_utc(input) == expout


def test_convert_sql_timestamp_to_utc_raises_error_if_date_passed_in_wrong_format():
    with pytest.raises(Exception) as ValueError:
        input = "1/1/2024"
        convert_sql_timestamp_to_utc(input)


def test_convert_utc_to_sql_timestamp_outputs_string_in_correct_format():
    input = "2024-01-01T000000000Z"
    expout = "2024-01-01 00:00:00.000"
    assert convert_utc_to_sql_timestamp(input) == expout


def test_convert_utc_to_sql_raises_error_if_date_passed_in_wrong_format():
    with pytest.raises(Exception) as ValueError:
        input = "1/1/2024"
        convert_utc_to_sql_timestamp(input)


def test_convert_datetime_to_utc_outputs_string_in_correct_format():
    input = datetime(2024, 1, 1, 0, 0, 0)
    expout = "2024-01-01T000000000Z"
    assert convert_datetime_to_utc(input) == expout


def test_convert_datetime_to_utc_raises_error_if_date_passed_in_wrong_format():
    with pytest.raises(Exception) as ValueError:
        input = "1/1/2024"
        convert_datetime_to_utc(input)
