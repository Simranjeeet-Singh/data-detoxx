from src.utils.file_reading_utils import list_files_from_s3
import boto3
from moto import mock_aws


@mock_aws
def test_returns_empty_list_of_file_names_inside_a_empty_bucket():
    s3 = boto3.client("s3", "us-east-1")
    s3.create_bucket(Bucket="my_bucket")

    result = list_files_from_s3("my_bucket")
    print(result)
    assert result == []


@mock_aws
def test_returns_file_names_inside_a_bucket():
    s3 = boto3.client("s3", "us-east-1")
    s3.create_bucket(Bucket="my_bucket")
    s3.put_object(Bucket="my_bucket", Key="testFile.txt")

    result = list_files_from_s3("my_bucket")
    print(result)
    assert result == ["testFile.txt"]


@mock_aws
def test_returns_list_of_csv_and_test_file_names_inside_bucket():
    s3 = boto3.client("s3", "us-east-1")
    s3.create_bucket(Bucket="my_bucket")
    s3.put_object(Bucket="my_bucket", Key="testFile.txt")
    s3.put_object(Bucket="my_bucket", Key="TABLE_NAME_[#1]_2009-08-08T121800Z.csv")

    result = list_files_from_s3("my_bucket")
    print(result)
    assert result == ["TABLE_NAME_[#1]_2009-08-08T121800Z.csv", "testFile.txt"]
