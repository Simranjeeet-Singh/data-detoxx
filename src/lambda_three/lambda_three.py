import boto3
import pyarrow.parquet as pq
from io import BytesIO

def read_parquet_from_processed_bucket(bucket_name):
    s3Client = boto3.client('s3')
    objects = s3Client.list_objects_v2(Bucket=bucket)
    for obj in objects['Contents']:
        key = objects['Key']
        if key.endswith('.parquet'):
            obj = s3Client.get_object(Bucket=bucket, Key=key)
        parquet_file = pq.ParquetFile(BytesIO(file_obj['Body'].read()))
        df = parquet_file.read().to_pandas()
    return df

def get_credentials():
    """
    This function should get the data warehouse credentials from aws secret manager"""
from botocore.exceptions import ClientError
import boto3
import ast

# INSTEAD OF CREATING THE FUNCTION CAN IMPORT INTO THE ACTUAL LAMBDA_THREE FILE
# from utils.extract_secrets import get_secret


def get_secret():

    secret_name = "database_credentials"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    return ast.literal_eval(get_secret_value_response["SecretString"])