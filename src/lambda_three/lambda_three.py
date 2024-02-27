import boto3
import pyarrow.parquet as pq
from io import BytesIO
from pg8000.native import Connection
from pg8000 import DatabaseError
from utils.extract_secrets import get_secret
from pprint import pprint
from utils.date_utils import convert_datetime_to_utc
import datetime
import pandas as pd


def connect():
    """
    Establishes a connection to a PostgreSQL database using credentials stored in AWS Secrets Manager.
    The function loads these variables from a .env file using dotenv, then uses them to create a pg8000.native
    Connection object.

    Returns:
        Connection: A pg8000.native Connection object connected to the specified PostgreSQL database.
    """

    secret_dict = get_secret("warehouse_credentials")
    try:
        conn = Connection(
            host=secret_dict["Hostname"],
            user=secret_dict["Username"],
            password=secret_dict["Password"],
            database=secret_dict["Database_name"],
            port=secret_dict["Port"],
        )
        client = boto3.client("s3")
        # response = client.list_objects_v2(Bucket='data-detox-processed-bucket', Prefix='dim_date')
        return conn
    except:
        raise DatabaseError

connect()

def lambda_handler3(event, context):
    pass


def read_parquet_from_processed_bucket(bucket_name, folder_name, filename):
    s3Client = boto3.client('s3')
    # objects = s3Client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    obj = s3Client.get_object(Bucket=bucket_name, Key=filename) # objects['Contents'][-1]['Key']
    parquet_file = pq.ParquetFile(BytesIO(obj['Body'].read()))
    df = parquet_file.read().to_pandas()
    print(df)
    return df

read_parquet_from_processed_bucket('data-detox-processed-bucket', 'dim_date', 'dim_date/dim_date__[#66]__2024-02-26T150109902Z.parquet')

# INSTEAD OF CREATING THE FUNCTION CAN IMPORT INTO THE ACTUAL LAMBDA_THREE FILE
# from utils.extract_secrets import get_secret