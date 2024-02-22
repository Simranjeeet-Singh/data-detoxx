from src.lambda_two.lambda_two import list_tablenames_from_s3
import pytest
from moto import mock_aws
import boto3

BUCKET_NAME = "test-bucket"
TABLE_NAME1 = "test_table1"
TABLE_NAME2 = "test_table2"


@pytest.fixture()
def set_up():
    with mock_aws():
        # Create a mock S3 bucket and upload test CSV files
        bucket_name = BUCKET_NAME
        table_name1 = TABLE_NAME1
        table_name2 = TABLE_NAME2
        s3_client = boto3.client("s3")
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-west-2",
            },
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name1 + "/file1.csv",
            Body='pippo',
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name2 + "/file2.csv",
            Body='baudo',
        )
        yield  # Need yield to prevent teardown


def test_list_tablenames_from_s3_single_file_per_table(set_up):
    # Call the function under test
    print("testing")
    tablenames = list_tablenames_from_s3(BUCKET_NAME)

    # Assert that tablenames contains all table names in bucket. Set is to make sure that order does not matter
    assert set(tablenames)==set(['test_table1','test_table2'])

@pytest.fixture()
def set_up_2():
    with mock_aws():
        # Create a mock S3 bucket and upload test CSV files
        bucket_name = BUCKET_NAME
        table_name1 = TABLE_NAME1
        table_name2 = TABLE_NAME2
        s3_client = boto3.client("s3")
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-west-2",
            },
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name1 + "/file1.csv",
            Body='pippo',
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name1 + "/file2.csv",
            Body='pippo',
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name2 + "/file2.csv",
            Body='baudo',
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name2 + "/file3.csv",
            Body='baudo',
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key='paperino' + "/file3.csv",
            Body='baudo',
        )
        yield  # Need yield to prevent teardown

def test_list_tablenames_from_s3_multiple_files_per_table(set_up_2):
    # Call the function under test
    print("testing")
    tablenames = list_tablenames_from_s3(BUCKET_NAME)

    # Assert that tablenames contains all table names in bucket. Set is to make sure that order does not matter
    assert set(tablenames)==set(['test_table1','test_table2','paperino'])