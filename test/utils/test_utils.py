from unittest.mock import patch
import pytest
import pandas as pd
from utils.file_reading_utils import (
    return_latest_counter_and_timestamp_from_filenames as rcat,
    list_files_from_s3,
    tables_reader_from_s3,
)


def test_rcat_extracts_counter_correctly():
    input = ["address__[#1]__2022-11-03T142049962Z.csv"]
    expout = 1
    assert rcat("address", input)[0] == expout


def test_rcat_extracts_date_correctly():
    input = ["address__[#1]__2022-11-03T142049962Z.csv"]
    expout = "2022-11-03 14:20:49.962"
    assert rcat("address", input)[1] == expout


def test_rcat_returns_highest_counter():
    input = [
        "address__[#1]__2022-11-03T142049962Z.csv",
        "address__[#0]__2021-11-03T142049962Z.csv",
    ]
    expout = 1
    assert rcat("address", input)[0] == expout


def test_rcat_returns_most_recent_date():
    input = [
        "address__[#4]__2022-11-03T142049962Z.csv",
        "address__[#3]__2021-11-03T142049962Z.csv",
        "address__[#2]__2020-11-03T142049962Z.csv",
        "address__[#1]__2019-11-03T142049962Z.csv",
    ]
    expout = "2022-11-03 14:20:49.962"
    assert rcat("address", input)[1] == expout


def mock_s3_list_objects_empty(Bucket):
    """
    Mocks an S3 client response for an empty bucket.
    """
    return {"ResponseMetadata": {"HTTPStatusCode": 200}}


def mock_s3_list_objects_with_files(Bucket):
    """
    Mocks an S3 client response for a bucket with files.
    """
    return {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Contents": [
            {"Key": "folder1/file1.txt"},
            {"Key": "folder2/file2.jpg"},
            {"Key": "file3.pdf"},
        ],
    }


@patch("boto3.client")
def test_list_files_from_s3_empty(mock_boto3_client):
    """
    Test the function with an empty bucket.
    """
    mock_boto3_client.return_value.list_objects.side_effect = mock_s3_list_objects_empty

    assert (
        list_files_from_s3("empty-bucket") == []
    ), "Expected an empty list for an empty bucket"


@patch("boto3.client")
def test_list_files_from_s3_with_files(mock_boto3_client):
    """
    Test the function with a bucket that has files.
    """
    mock_boto3_client.return_value.list_objects.side_effect = (
        mock_s3_list_objects_with_files
    )

    expected_files = ["file1.txt", "file2.jpg", "file3.pdf"]
    assert (
        list_files_from_s3("bucket-with-files") == expected_files
    ), "Expected a list of filenames in the bucket"


def test_return_latest_counter_and_timestamp_from_filenames_c_raises_error_if_address_passed_in_wrong_format():
    with pytest.raises(Exception) as ValueError:
        input = ["address__[#2]__2022-11-03T142049962Z.csv"]
        test_return_latest_counter_and_timestamp_from_filenames_c_raises_error_if_address_passed_in_wrong_format(
            input
        )


# def side_effect_getdf(bucketname, tablename, counter_start=1):
#     match tablename:
#         case 'payment':
#             return pd.DataFrame([{'test':10, 'test2':20}])
#         case 'address':
#             return pd.DataFrame([{'test':100, 'test2':200}])
#         case _:
#             return pd.DataFrame()
# def side_effect_latest_counter(tablename, tablename_files):
#     match tablename:
#         case 'payment':
#             return (2,'2024-02-23T181210139Z')
#         case 'address':
#             return (1,'2024-02-23T181210137Z')
#         case _:
#             return (1,'2024-02-23T181210137Z')

# def side_eff_statefile(bucketname):
#     return {'payment':True, 'address':True}

# @patch('utils.file_reading_utils.get_dataframe_from_s3')
# def test_file_reader(mock_getdf):
#     with patch('utils.file_reading_utils.return_latest_counter_and_timestamp_from_filenames') as mock_ctr:
#         with patch('utils.state_file.read_state_file_from_s3') as mock_state:
#             mock_getdf.side_effect = side_effect_getdf
#             mock_ctr.side_effect = side_effect_latest_counter
#             mock_state.side_effect = side_eff_statefile
#             print(mock_state('kek'))
#             tablenames=['payment/payment__[#1]__2024-02-23T181210137Z.csv','payment/payment__[#2]__2024-02-23T181210139Z.csv','address/address__[#1]__2024-02-23T181210137Z.csv']
#             result=tables_reader_from_s3(tablenames,'mock_bucket')

#     exp_res=({'payment':pd.DataFrame([{'test':10, 'test2':20}]), 'address':pd.DataFrame([{'test':100, 'test2':200}])},{'payment':(2,'2024-02-23T181210139Z'),'address':(1,'2024-02-23T181210137Z')})

#     assert result[1]['payment']==exp_res[1]['payment']
#     assert result[1]['address']==exp_res[1]['address']
#     assert (result[0]['payment']==exp_res[0]['payment']).all().all()
#     assert (result[0]['address']==exp_res[0]['address']).all().all()
