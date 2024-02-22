import pytest
import pandas as pd
from moto import mock_aws
import boto3

from src.utils.utils import get_dataframe_from_s3


BUCKET_NAME = "test-bucket"
TABLE_NAME = "test_table"


@pytest.fixture(autouse=True)
def set_up():
    with mock_aws():
        # Create a mock S3 bucket and upload test CSV files
        bucket_name = BUCKET_NAME
        table_name = TABLE_NAME

        filename1 = f"{table_name}__[#1]__2022-11-03T142049962Z.csv"
        filename2 = f"{table_name}__[#2]__2022-11-04T142049962Z.csv"
        filename3 = f"{table_name}__[#2]__2022-11-05T142049962Z.csv"

        pd1 = pd.DataFrame({"A": [1], "B": [1]})
        pd2 = pd.DataFrame({"A": [2, 3], "B": [2, 3]})
        pd3 = pd.DataFrame({"A": [4, 5, 6], "B": [4, 5, 6]})

        s3_client = boto3.client("s3")
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "eu-west-2",
            },
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name + "/" + filename1,
            Body=pd1.to_csv(index=False),
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name + "/" + filename2,
            Body=pd2.to_csv(index=False),
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key=table_name + "/" + filename3,
            Body=pd3.to_csv(index=False),
        )
        # Need yield to prevent teardown
        yield {
            "filenames": [filename1, filename2, filename3],
            "csv_data": [pd1, pd2, pd3],
        }


def test_get_dataframe_from_s3_with_empty_bucket():
    # Having this test first also tests that moto state does not persist between tests
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.objects.all().delete()

    df = get_dataframe_from_s3(BUCKET_NAME, TABLE_NAME)
    assert df == None


def test_get_dataframe_from_s3_returns_correct_dataframe():
    df = get_dataframe_from_s3(BUCKET_NAME, TABLE_NAME)
    values_list = list(range(1, 7))
    expected_dict = {"A": values_list, "B": values_list}
    df_to_dict = df.to_dict(orient="list")

    assert df_to_dict == expected_dict


# def test_get_dataframe_from_s3_with_counter_start():
#     df = get_dataframe_from_s3(BUCKET_NAME, TABLE_NAME, counter_start=2)
#     expected_dict = {"A": [2, 3, 4, 5, 6], "B": [2, 3, 4, 5, 6]}
#     df_to_dict = df.to_dict(orient="list")
#     assert df_to_dict == expected_dict


# def test_get_dataframe_from_s3_with_counter_end():
#     df = get_dataframe_from_s3(BUCKET_NAME, TABLE_NAME, counter_end=2)
#     expected_dict = {"A": [1, 2], "B": [1, 2]}
#     df_to_dict = df.to_dict(orient="list")
#     assert df_to_dict == expected_dict

# def test_get_dataframe_from_s3_with_counter_start_end():
#     df = get_dataframe_from_s3(BUCKET_NAME, TABLE_NAME, counter_start=1, counter_end=3)
#     expected_dict = {"A": [2, 3, 4], "B": [2, 3, 4]}
#     df_to_dict = df.to_dict(orient="list")
#     assert df_to_dict == expected_dict


def test_get_dataframe_from_s3_with_nonexistent_table():
    df = get_dataframe_from_s3(BUCKET_NAME, "nonexistent_table")
    assert df is None


def test_get_dataframe_from_s3_with_single_file(set_up):
    filenames_to_delete = set_up["filenames"]
    filenames_to_delete.pop()

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.delete_objects(
        Delete={
            "Objects": [
                {"Key": TABLE_NAME + "/" + filename} for filename in filenames_to_delete
            ]
        }
    )

    df = get_dataframe_from_s3(BUCKET_NAME, TABLE_NAME)
    expected_dict = {"A": [4, 5, 6], "B": [4, 5, 6]}
    df_to_dict = df.to_dict(orient="list")
    assert df_to_dict == expected_dict


# def test_get_dataframe_from_s3_with_invalid_csv():
#     s3_client = boto3.client("s3")
#     table_name = "invalid_csv_table"
#     filename = f"{table_name}__[#1]__2022-11-03T142049962Z.csv"
#     invalid_csv_data = "invalid,csv,format\n1,2,3\n4,5,6"  # Invalid CSV format
#     s3_client.put_object(
#         Bucket=BUCKET_NAME,
#         Key=table_name + "/" + filename,
#         Body=invalid_csv_data,
#     )

#     df = get_dataframe_from_s3(BUCKET_NAME, table_name)
#     assert df is None


if __name__ == "__main__":
    pytest.main([__file__])
