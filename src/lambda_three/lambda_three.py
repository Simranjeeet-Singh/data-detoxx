import boto3
import pyarrow.parquet as pq
from io import BytesIO
from pg8000.native import Connection
from pg8000 import DatabaseError
from utils.extract_secrets import get_secret
from utils.date_utils import convert_datetime_to_utc
import datetime
import pandas as pd
import logging
from utils.state_file import read_state_file_from_s3
from utils.file_reading_utils import return_latest_counter_and_timestamp_from_filenames, get_parquet_dataframe_from_s3, list_files_from_s3_folder


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
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    logger.error('rcd10')
    raise RuntimeError


def read_updated_tables_from_s3(bucket_name: str) -> dict[pd.DataFrame]:
    updated_dataframes = {}
    updated_tables_dict = read_state_file_from_s3(bucket_name)

    for table_name in updated_tables_dict:
        if updated_tables_dict[table_name]: # if table has been updated
            list_of_filenames = list_files_from_s3_folder(bucket_name, table_name)
            counter, _ = return_latest_counter_and_timestamp_from_filenames(table_name, list_of_filenames)
            df = get_parquet_dataframe_from_s3(bucket_name, table_name, counter)
            updated_dataframes[table_name] = df

    print(updated_dataframes)
    return updated_dataframes

# def read_parquet_from_processed_bucket(bucket_name, folder_name, filename):
#     s3Client = boto3.client('s3')
#     # objects = s3Client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
#     obj = s3Client.get_object(Bucket=bucket_name, Key=filename) # objects['Contents'][-1]['Key']
#     parquet_file = pq.ParquetFile(BytesIO(obj['Body'].read()))
#     df = parquet_file.read().to_pandas()
#     print(df)
#     return df








read_updated_tables_from_s3('data-detox-processed-bucket')