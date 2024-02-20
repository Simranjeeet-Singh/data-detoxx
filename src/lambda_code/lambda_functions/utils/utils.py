import boto3
from date_utils import convert_utc_to_sql_timestamp
import pandas as pd


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
    counter_timestamp_dict = {}

    if not filenames:
        return 0, None

    # Extract counter and timestamp from filenames into dict
    for filename in filenames:
        table_name, counter, datetime = filename.split("__")
        counter = int(counter.strip("[]").replace("#", ""))
        if table_name == target_table_name:
            if counter in counter_timestamp_dict:
                raise ValueError("Duplicate counter values exist in filenames")
            else:
                counter_timestamp_dict[counter] = datetime

    largest_counter = max(counter_timestamp_dict.keys())
    sql_datetime = convert_utc_to_sql_timestamp(
        counter_timestamp_dict[largest_counter].strip(".csv")
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
    return [item["Key"].split("/")[-1] for item in response["Contents"]]


def return_counter_filename_dict_from_filenames(
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
    counter_timestamp_dict = {}

    if not filenames:
        return 0, None

    # Extract counter and timestamp from filenames into dict
    for filename in filenames:
        table_name, counter, datetime = filename.split("__")
        counter = int(counter.strip("[]").replace("#", ""))
        if table_name == target_table_name:
            if counter in counter_timestamp_dict:
                raise ValueError("Duplicate counter values exist in filenames")
            else:
                counter_timestamp_dict[counter] = datetime

    largest_counter = max(counter_timestamp_dict.keys())
    sql_datetime = convert_utc_to_sql_timestamp(
        counter_timestamp_dict[largest_counter].strip(".csv")
    )
    return (largest_counter, sql_datetime)


def get_dataframe_from_s3(
    bucket_name: str,
    table_name: str,
    counter_start: int = None,
    counter_end: int = None,
) -> pd.DataFrame:
    """
    Fetches CSV files from an S3 bucket's folder titled 'table_name', concatenates them into a single DataFrame, and saves the DataFrame to a CSV file.

    Parameters:
    - bucket_name (str): The name of the S3 bucket.
    - table_name (str): The name of the folder in the S3 bucket containing the CSV files.
    - counter_start (int, optional): The starting index of the CSV files to fetch. Defaults to None, which starts from the first file.
    - counter_end (int, optional): The ending index (exclusive) of the CSV files to fetch. Defaults to None, which fetches until the last file.

    Returns:
    - pd.DataFrame: A DataFrame containing the concatenated data from all CSV files.

    The function fetches CSV files from the specified S3 folder, concatenates them into a single DataFrame, and saves the DataFrame to a CSV file named 'table_name.csv' in the current working directory.

    Example:
    df = get_dataframe_from_s3(bucket_name='my_bucket', table_name='my_folder', counter_start=0, counter_end=5)
    """

    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=table_name)
    table_s3_keys = [item["Key"] for item in response["Contents"]]
    dfs = []
    for s3_key in table_s3_keys[counter_start:counter_end]:
        response = client.get_object(Bucket=bucket_name, Key=s3_key)
        csv_data = pd.read_csv(response["Body"])
        dfs.append(csv_data)

    concatenated_df = pd.concat(dfs, ignore_index=True)
    # concatenated_df.to_csv(table_name + ".csv", index=False)
    return concatenated_df


if __name__ == "__main__":
    # filenames = ["mytable_[#1]_2009-08-08T121800Z", "mytable_[#2]_2009-08-08T1218020Z"]
    # print(return_latest_counter_and_timestamp_from_filenames("mytable", filenames))
    # print(return_latest_counter_and_timestamp_from_filenames("mytable", []))
    # print(list_files_from_s3("data-detox-ingestion-bucket"))
    get_dataframe_from_s3("data-detox-ingestion-bucket", "sales_order")
    # get_tables_from_s3("data-detox-ingestion-bucket", "sales_order")
