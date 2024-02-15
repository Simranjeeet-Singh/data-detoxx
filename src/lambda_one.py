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
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    try:
        connection = connect()
        csv_paths = save_db_to_csv(connection, logger)
        connection.close()
        s3 = boto3.client("s3")
        for path in csv_paths:
            s3.upload_file(Filename=path, Bucket=BUCKET_NAME, Key=path)

    except ClientError as c:
        print(c)
        if c.response["Error"]["Code"] == "NoSuchBucket":
            logger.error(f"No such bucket - {BUCKET_NAME}")
    except Exception as e:
        logger.error(e)
        raise RuntimeError


if __name__ == "__main__":
    lambda_handler("test", "context")
