import boto3
from utils.date_utils import (
    convert_utc_to_sql_timestamp,
)
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO
import logging
from utils.state_file import read_state_file_from_s3


class WrongFilesIngestionBucket(Exception):
    pass


def return_latest_counter_and_timestamp_from_filenames(
    target_table_name: str, filenames: list[str]
) -> tuple[int, str]:
    """
    Extracts the latest counter and corresponding timestamp from a list of filenames for a specific table.

    Args:
        target_table_name (str): The name of the target table.
        filenames (list[str]): A list of filenames.

    Returns:
        Tuple (largest_counter: int, sql_datetime: str):
        A tuple containing the largest counter and its corresponding timestamp in the following format 'YYYY-MM-DD HH:MM:SS.SSS'.
    """

    if not filenames:
        return 0, None
    counter_timestamp_dict, *discard_values = extract_counter_from_filenames(
        filenames, target_table_name
    )
    largest_counter = max(counter_timestamp_dict.keys())
    sql_datetime = convert_utc_to_sql_timestamp(
        counter_timestamp_dict[largest_counter].strip(".csv").strip(".parquet")
    )
    return (largest_counter, sql_datetime)


def list_files_from_s3(bucket_name: str) -> list[str]:
    """
    Args : bucket_name as a `string` \n
    Returns : list of file names inside the bucket as `list` of `strings`
    """
    client = boto3.client("s3")
    response = client.list_objects(Bucket=bucket_name)
    if "Contents" not in response:
        return []
    return [
        item["Key"].split("/")[-1]
        for item in response["Contents"]
        if item["Key"] != "state_file.json"
    ]


def list_files_from_s3_folder(bucket_name: str, folder_name: str) -> list[str]:
    """
    Args : bucket_name as a `string` \n
    Returns : list of file names inside the bucket as `list` of `strings`
    """
    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    if "Contents" not in response:
        return []
    return [
        item["Key"].split("/")[-1]
        for item in response["Contents"]
        if item["Key"] != "state_file.json"
    ]


def extract_counter_from_filenames(
    filenames: list[str], target_table_name: str = None
) -> tuple[dict[int, str], dict[int, str]]:
    """
    Extracts counters and timestamps from a list of filenames and returns a tuple:

    1. A dictionary mapping counter values to corresponding timestamps.
    2. A dictionary mapping counter values to corresponding filenames.

    Args:
        filenames (List[str]): A list of filenames in the format 'table_name__counter__datetime'.
        target_table_name (Optional[str]): The specific table name to filter filenames by (default is None).

    Returns:
        counter_timestamp_mapping, counter_filename_mapping

    Raises:
        WrongFilesIngestionBucket: If any of the filenames are not in the expected format.
        ValueError: If duplicate counter values exist in filenames.
    """
    counter_timestamp_mapping = {}
    counter_filename_mapping = {}
    for filename in filenames:
        try:
            table_name, counter, datetime = filename.split("__")
            counter = int(counter.strip("[]").replace("#", ""))
            if target_table_name is None or table_name == target_table_name:
                # if counter in counter_timestamp_mapping:
                #     print(counter, table_name)
                #     raise ValueError("Duplicate counter values exist in filenames")
                # else:
                counter_timestamp_mapping[counter] = datetime
                counter_filename_mapping[counter] = filename
        except ValueError as e:
            # logger.error(e)
            if filename == "state_file.json":
                pass
            else:
                raise
    return counter_timestamp_mapping, counter_filename_mapping


def get_dataframe_from_s3(
    bucket_name: str,
    table_name: str,
    counter_start: int = 0,
    counter_end: int = float("inf"),
) -> pd.DataFrame | None:
    """
    Reads CSV files from an S3 bucket's folder titled table_name, concatenates them and returns a single pd.DataFrame. If no .csv files are found, returns None.

    Parameters:
    - bucket_name (str): The name of the S3 bucket.
    - table_name (str): The name of the folder in the S3 bucket containing the CSV files.
    - counter_start (int, optional): The starting index of the CSV files to fetch. Defaults to None, which starts from the first file.
    - counter_end (int, optional): The ending index (exclusive) of the CSV files to fetch. Defaults to None, which fetches until the last file.

    Returns:
    - pd.DataFrame: A DataFrame containing the concatenated data from all CSV files.

    The function fetches CSV files from the specified S3 folder, concatenates them into a single DataFrame.

    Raises:
    WrongFilesIngestionBucket: If any of the filenames are not in the expected format, duplicate counters, any of the column names of the csv are not identical.

    Example:
    df = get_dataframe_from_s3(bucket_name='my_bucket', table_name='my_folder', counter_start=0, counter_end=5)
    """

    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=table_name)
    if response["KeyCount"] == 0:
        return None

    table_s3_keys_all = [item["Key"] for item in response["Contents"]]
    dfs = []
    table_s3_keys_to_read = []

    _, counter_to_filename_mapping = extract_counter_from_filenames(table_s3_keys_all)

    if counter_start == 0 and counter_end == float("inf"):
        # Read all keys
        table_s3_keys_to_read = table_s3_keys_all

    else:
        # Read only keys between counter_start and counter_end
        for counter in counter_to_filename_mapping.keys():
            if counter_start <= counter < counter_end:
                table_s3_keys_to_read.append(counter_to_filename_mapping[counter])

    for s3_key in table_s3_keys_to_read:
        response = client.get_object(Bucket=bucket_name, Key=s3_key)
        csv_data = pd.read_csv(response["Body"])
        dfs.append(csv_data)

    if check_all_df_columns_are_identical(dfs):
        concatenated_df = pd.concat(dfs)
        return concatenated_df
    else:
        raise ValueError("Cannot concat dataframes if column are not identical")


def get_parquet_dataframe_from_s3(
    bucket_name: str,
    table_name: str,
    counter_start: int = 0,
    counter_end: int = float("inf"),
) -> pd.DataFrame | None:

    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=table_name)
    if response["KeyCount"] == 0:
        return None

    table_s3_keys_all = [item["Key"] for item in response["Contents"]]
    table_s3_keys_to_read = []

    _, counter_to_filename_mapping = extract_counter_from_filenames(table_s3_keys_all)

    if counter_start == 0 and counter_end == float("inf"):
        # Read all keys
        table_s3_keys_to_read = table_s3_keys_all

    else:
        # Read only keys between counter_start and counter_end
        for counter in counter_to_filename_mapping.keys():
            if counter_start <= counter < counter_end:
                table_s3_keys_to_read.append(counter_to_filename_mapping[counter])

    for s3_key in table_s3_keys_to_read:
        response = client.get_object(Bucket=bucket_name, Key=s3_key)
        parquet_file = pq.ParquetFile(BytesIO(response["Body"].read()))
        parquet_data = parquet_file.read().to_pandas()
        return parquet_data


def check_all_df_columns_are_identical(dataframes: list[pd.DataFrame]) -> bool:
    """
    Check if all columns in a list of DataFrames have identical names.

    Parameters:
        dataframes (List[pd.DataFrame]): A list of pandas DataFrames to check.

    Returns:
        bool: True if all DataFrames have identical column names, False otherwise.
    """
    # Get the column names of the first DataFrame
    reference_columns = dataframes[0].columns.tolist()

    # Check if all other DataFrames have identical columns
    for df in dataframes[1:]:
        if df.columns.tolist() != reference_columns:
            return False
    return True


def path_to_parquet(table_name: str, counter: int, last_updated: str) -> str:
    """
    Generates a file path for storing a Parquet file.

    Args:
        `table_name`: The name of the table.
        `counter`: An integer counter for versioning or distinguishing files.

    Returns:
        `str`: A string representing the file path in the format:
            "{table_name}/{table_name}__[#{counter}]__{date}.parquet"
            where {table_name} is the name of the table,
            {counter} is the version or counter value,
            and {date} is the current UTC datetime converted to string.
    """
    return f"{table_name}/{table_name}__[#{counter}]__{last_updated}.parquet"


def tables_reader_from_s3(
    tables: list, bucketname: str
) -> tuple[dict[str, pd.DataFrame], dict[str, tuple[int, str]]]:
    """
    Reads tables data from S3 bucket, taking the last written file for most tables, and returns dataframes along with their latest counter and timestamp.
    For the non-updating tables, it always retrieves all the data in the s3 bucket.

    Parameters:
        tables (list): List of table names with counters appended in the format 'tablename__counter'.
        bucketname (str): Name of the S3 bucket.

    Returns:
        Tuple[Dict[str, pd.DataFrame], Dict[str, Tuple[int, str]]]: A tuple containing two dictionaries:
            - First dictionary maps table names to their corresponding dataframes.
            - Second dictionary maps table names to a tuple containing the latest counter and latest timestamp.
    """
    tablenames = list(set([element.split("__")[0].split("/")[0] for element in tables]))
    dataframes, counters_dates = {}, {}
    dependent_tables = [
        "department",
        "counterparty",
        "currency",
        "payment_type",
        "address",
        'sales_order'
    ]  # The .csv files for these tables are always all read and stored in a single .parquet file
    for tablename in tablenames:
        if tablename in dependent_tables:
            df = get_dataframe_from_s3(
                bucketname, tablename
            )  # get all .csv files from ingestion bucket
            tablename_files = [
                element
                for element in tables
                if element.split("__")[0].split("/")[0] == tablename
            ]
            tb_counters_dates = return_latest_counter_and_timestamp_from_filenames(
                tablename, tablename_files
            )
        else:
            dict = read_state_file_from_s3(bucketname)
            if dict[tablename]:
                tablename_files = [
                    element
                    for element in tables
                    if element.split("__")[0].split("/")[0] == tablename
                ]
                tb_counters_dates = return_latest_counter_and_timestamp_from_filenames(
                    tablename, tablename_files
                )
                df = get_dataframe_from_s3(
                    bucketname, tablename, counter_start=tb_counters_dates[0]
                )
            else:
                continue
        dataframes[tablename] = df
        counters_dates[tablename] = tb_counters_dates
    if len(dataframes.keys()) == len(counters_dates.keys()):
        return dataframes, counters_dates
    else:
        raise RuntimeError(
            "There has been a problem in retrieving versioning of files in the ingestion bucket."
        )


if __name__ == "__main__":
    # filenames = ["mytable_[#1]_2009-08-08T121800Z", "mytable_[#2]_2009-08-08T1218020Z"]
    # print(return_latest_counter_and_timestamp_from_filenames("mytable", filenames))
    # print(return_latest_counter_and_timestamp_from_filenames("mytable", []))
    # print(list_files_from_s3("data-detox-ingestion-bucket"))
    get_dataframe_from_s3("data-detox-ingestion-bucket", "sales_order")
    # get_tables_from_s3("data-detox-ingestion-bucket", "sales_order")
