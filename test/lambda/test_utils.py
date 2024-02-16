from unittest.mock import patch, MagicMock
from src.lambda_functions.utils.utils import (
    return_latest_counter_and_timestamp_from_filenames as rcat, list_files_from_s3)


def test_rcat_extracts_counter_correctly():
    input = ['address__[#1]__2022-11-03T142049962Z.csv']
    expout = 1
    assert rcat('address', input)[0] == expout


def test_rcat_extracts_date_correctly():
    input = ['address__[#1]__2022-11-03T142049962Z.csv']
    expout = '2022-11-03 14:20:49.962'
    assert rcat('address', input)[1] == expout


def test_rcat_returns_highest_counter():
    input = ['address__[#1]__2022-11-03T142049962Z.csv',
             'address__[#0]__2021-11-03T142049962Z.csv']
    expout = 1
    assert rcat('address', input)[0] == expout


def test_rcat_returns_most_recent_date():
    input = ['address__[#4]__2022-11-03T142049962Z.csv',
             'address__[#3]__2021-11-03T142049962Z.csv', 'address__[#2]__2020-11-03T142049962Z.csv',
             'address__[#1]__2019-11-03T142049962Z.csv']
    expout = '2022-11-03 14:20:49.962'
    assert rcat('address', input)[1] == expout


def mock_s3_list_objects_empty(Bucket):
    """
    Mocks an S3 client response for an empty bucket.
    """
    return {
        'ResponseMetadata': {
            'HTTPStatusCode': 200
        }
    }


def mock_s3_list_objects_with_files(Bucket):
    """
    Mocks an S3 client response for a bucket with files.
    """
    return {
        'ResponseMetadata': {
            'HTTPStatusCode': 200
        },
        'Contents': [
            {'Key': 'folder1/file1.txt'},
            {'Key': 'folder2/file2.jpg'},
            {'Key': 'file3.pdf'},
        ]
    }


@patch('boto3.client')
def test_list_files_from_s3_empty(mock_boto3_client):
    """
    Test the function with an empty bucket.
    """
    mock_boto3_client.return_value.list_objects.side_effect = mock_s3_list_objects_empty

    assert list_files_from_s3(
        "empty-bucket") == [], "Expected an empty list for an empty bucket"


@patch('boto3.client')
def test_list_files_from_s3_with_files(mock_boto3_client):
    """
    Test the function with a bucket that has files.
    """
    mock_boto3_client.return_value.list_objects.side_effect = mock_s3_list_objects_with_files

    expected_files = ['file1.txt', 'file2.jpg', 'file3.pdf']
    assert list_files_from_s3(
        "bucket-with-files") == expected_files, "Expected a list of filenames in the bucket"
