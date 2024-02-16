from lambda_functions.utils.date_utils import convert_utc_to_sql_timestamp
import boto3


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
    sql_datetime = convert_utc_to_sql_timestamp(counter_timestamp_dict[largest_counter].strip(".csv"))
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
    return [item["Key"].split('/')[-1] for item in response["Contents"]]


if __name__ == "__main__":
    filenames = ["mytable_[#1]_2009-08-08T121800Z", "mytable_[#2]_2009-08-08T1218020Z"]
    print(return_latest_counter_and_timestamp_from_filenames("mytable", filenames))
    print(return_latest_counter_and_timestamp_from_filenames("mytable", []))
