from src.lambda_functions.utils.utils import (
    return_latest_counter_and_timestamp_from_filenames as rcat)


def test_extracts_counter_correctly():
    input = ['address__[#1]__2022-11-03T142049962Z.csv',
             'address__[#0]__2021-11-03T142049962Z.csv']
    expout = 1
    assert rcat('address', input)[0] == expout
