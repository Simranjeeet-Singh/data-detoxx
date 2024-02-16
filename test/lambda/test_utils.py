from src.lambda_functions.utils.utils import (
    return_latest_counter_and_timestamp_from_filenames as rcat)


def test_extracts_counter_correctly():
    input = ['address_[#1]_2022-11-03T142049962Z.csv']
    expout = 1
    assert rcat('test', input)[0] == expout
