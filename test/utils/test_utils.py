from unittest.mock import patch
import pytest
import pandas as pd
from utils.file_reading_utils import (
    return_latest_counter_and_timestamp_from_filenames as rcat,
    list_files_from_s3, tables_reader_from_s3
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

def side_effect_getdf(bucketname, tablename, counter_start=1):
    match tablename:
        case 'table':
            return pd.DataFrame([{'test':10, 'test2':20}])
        case 'table2':
            return pd.DataFrame([{'test':100, 'test2':200}])
def side_effect_latest_counter(tablename, tablename_files):
    match tablename:
        case 'table':
            return (2,'2024-02-23T181210139Z')
        case 'table2':
            return (1,'2024-02-23T181210137Z')
        
@patch('utils.file_reading_utils.get_dataframe_from_s3')
def test_file_reader(mock_getdf):
    with patch('utils.file_reading_utils.return_latest_counter_and_timestamp_from_filenames') as mock_ctr:
        mock_getdf.side_effect = side_effect_getdf
        mock_ctr.side_effect = side_effect_latest_counter
        tablenames=['table/table__[#1]__2024-02-23T181210137Z.csv','table/table__[#2]__2024-02-23T181210139Z.csv','table2/table2__[#1]__2024-02-23T181210137Z.csv']
        result=tables_reader_from_s3(tablenames,'mock_bucket')

    exp_res=({'table':pd.DataFrame([{'test':10, 'test2':20}]), 'table2':pd.DataFrame([{'test':100, 'test2':200}])},{'table':(2,'2024-02-23T181210139Z'),'table2':(1,'2024-02-23T181210137Z')})
    
    assert result[1]==exp_res[1]
    assert (result[0]['table']==exp_res[0]['table']).all().all()
    assert (result[0]['table2']==exp_res[0]['table2']).all().all()