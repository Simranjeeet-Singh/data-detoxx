import boto3

from pg8000.native import Connection
from pg8000 import DatabaseError
from utils.extract_secrets import get_secret
import pandas as pd
import logging
from utils.state_file import read_state_file_from_s3
from utils.file_reading_utils import (
    return_latest_counter_and_timestamp_from_filenames,
    get_parquet_dataframe_from_s3,
    list_files_from_s3_folder,
)
from lambda_functions.insert_dataframe_into_warehouse import (
    insert_dataframes_into_warehouse,
)

BUCKET_NAME = "data-detox-processed-bucket"


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


def lambda_handler3(event, context):
    """
    It initializes a logger, connects to the final PostgreSQL Warehouse,
    extracts data from last updated parquet file in processed bucket,
    and inserts extracted data into the Warehouse.

    Parameters:
    - event: The event data (not used in this function, but required by AWS Lambda).
    - context: The runtime context of the lambda (not used in this function, but required by AWS Lambda).
    """
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    # logger.error("rcd10")
    try:
        connection = connect()
        updated_dfs_dict = read_updated_tables_from_s3(BUCKET_NAME)
        # print(updated_dfs_dict)
        if updated_dfs_dict:
            insert_dataframes_into_warehouse(connection, updated_dfs_dict)
        else:
            print("No updated dfs")

    except Exception as e:
        logger.error(e)
        raise RuntimeError


def read_updated_tables_from_s3(bucket_name: str) -> dict[pd.DataFrame]:
    updated_dataframes = {}
    # updated_tables_dict = read_state_file_from_s3(bucket_name)

    # FOR DEBUGGING ONLY
    updated_tables_dict = {
        "fact_sales_order": False,
        "dim_date": False,
        "dim_staff": False,
        "dim_design": False,
        "dim_transaction": False,
        "fact_purchase_order": False,
        "fact_payment": True,
        "dim_payment_type": True,
        "dim_currency": True,
        "dim_counterparty": True,
        "dim_location": True,
    }

    for table_name in updated_tables_dict:
        # if table has been updated
        if updated_tables_dict[table_name]:
            # list all the files in specified table's AWS folder
            list_of_filenames = list_files_from_s3_folder(bucket_name, table_name)
            # extract lastest counter from the list of filenames
            counter, _ = return_latest_counter_and_timestamp_from_filenames(
                table_name, list_of_filenames
            )
            # convert latest parquet file to dataframe
            df = get_parquet_dataframe_from_s3(bucket_name, table_name, counter)
            # put each dataframe as key value pair in updated_dataframes
            updated_dataframes[table_name] = df

    # print(updated_dataframes)
    return updated_dataframes


if __name__ == "__main__":
    lambda_handler3("test", "context")
