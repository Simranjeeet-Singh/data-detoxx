import logging
import boto3


def lambda_handler2(event, context):
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    logger.error("error")
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="data-detox-processed-bucket", Key="s3_key.txt", Body="file_data"
    )
    raise RuntimeError
