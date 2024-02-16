import logging
import boto3
from botocore.exceptions import ClientError
import csv
from pg8000.native import Connection
from lambda_functions.extraction_lambda import save_db_to_csv
from dotenv import load_dotenv
import os

# CHANGE BUCKET NAME
BUCKET_NAME = "mycsvbucket-nc"


def connect():
    """
    Establishes a connection to a PostgreSQL database using credentials stored in environment variables. 
    The function loads these variables from a .env file using dotenv, then uses them to create a pg8000.native 
    Connection object.

    Returns:
        Connection: A pg8000.native Connection object connected to the specified PostgreSQL database.
    """
    load_dotenv()
    conn = Connection(
        host=os.environ["Hostname"],
        user=os.environ["Username"],
        password=os.environ["Password"],
        database=os.environ["Database_name"],
        port=os.environ["Port"],
    )
    return conn


def lambda_handler(event, context):
    """
    Acts as the entry point for the AWS Lambda function. It initializes a logger, connects to a PostgreSQL 
    database, extracts data into CSV files, and uploads these files to an AWS S3 bucket. The function handles 
    exceptions by logging them and can raise a RuntimeError for unexpected errors.

    Parameters:
    - event: The event data (not used in this function, but required by AWS Lambda).
    - context: The runtime context of the lambda (not used in this function, but required by AWS Lambda).
    """
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    try:
        connection = connect()
        csv_paths = save_db_to_csv(connection, logger, BUCKET_NAME)
        connection.close()
        s3 = boto3.client("s3")
        for path in csv_paths:
            try:
                s3.upload_file(
                    Filename=f'tmp/{path}', Bucket=BUCKET_NAME, Key=path)
            except FileNotFoundError:
                tab_name = path.split('__')[0]
                logger.info(f'No rows added or modified to table {tab_name}')

    except ClientError as c:
        print(c)
        if c.response["Error"]["Code"] == "NoSuchBucket":
            logger.error(f"No such bucket - {BUCKET_NAME}")
    except Exception as e:
        logger.error(e)
        raise RuntimeError


if __name__ == "__main__":
    lambda_handler("test", "context")
