import boto3
import pyarrow.parquet as pq
from io import BytesIO
from pg8000.native import Connection
from pg8000 import DatabaseError
from utils.extract_secrets import get_secret


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
        # print(conn.run(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'project_team_4' AND table_type = 'BASE TABLE'"))
        return conn
    except:
        raise DatabaseError



def lambda_handler3(event, context):
    pass


# def read_parquet_from_processed_bucket(bucket_name):
#     s3Client = boto3.client('s3')
#     objects = s3Client.list_objects_v2(Bucket=bucket)
#     for obj in objects['Contents']:
#         key = objects['Key']
#         if key.endswith('.parquet'):
#             obj = s3Client.get_object(Bucket=bucket, Key=key)
#         parquet_file = pq.ParquetFile(BytesIO(file_obj['Body'].read()))
#         df = parquet_file.read().to_pandas()
#     return df

# INSTEAD OF CREATING THE FUNCTION CAN IMPORT INTO THE ACTUAL LAMBDA_THREE FILE
# from utils.extract_secrets import get_secret