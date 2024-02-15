import logging
import boto3
from botocore.exceptions import ClientError
import csv
from pg8000.native import Connection


logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

# CHANGE BUCKET NAME
BUCKET_NAME = "data-detox-ingestion-bucket"


def connect():
    con = Connection(
        host="nc-data-eng-totesys-production.chpsczt8h1nu.eu-west-2.rds.amazonaws.com",
        user="project_team_4",
        password="0zGVeR63AcJdktyt",
        database="totesys",
        port="5432",
    )
    sql_query = f"SELECT * FROM currency;"
    sql_results = con.run(sql_query)
    con.close()
    return sql_results


def lambda_handler(event, context):

    try:
        sql_results = connect()
        logger.info(f"event = {event}")
        logger.info(f"Sql results received {sql_results}")

        save_sql_query_list_to_csv(sql_results, "/tmp/sql_results.csv")

        s3 = boto3.client("s3")
        s3.upload_file("/tmp/sql_results.csv", BUCKET_NAME, "sql_results.csv")

    except ClientError as c:
        print(c)
        if c.response["Error"]["Code"] == "NoSuchBucket":
            logger.error(f"No such bucket - {BUCKET_NAME}")
    except Exception as e:
        logger.error(e)
        raise RuntimeError


def save_sql_query_list_to_csv(list_of_lists: list[list[str]], filename: str) -> None:
    """
    Save a list of lists to a CSV file.

    Args:
        list_of_lists (List[List[str]]): List of lists to be saved to CSV.
        filename (str): Name of the CSV file to be saved.

    Returns:
        None
    """
    if not list_of_lists:
        print("The list of lists is empty. Nothing to save.")
        return

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_of_lists)


if __name__ == "__main__":
    lambda_handler("test", "context")
