import boto3
import logging
import pandas as pd
from pathlib import Path
from utils.file_reading_utils import path_to_parquet
from utils.date_utils import convert_sql_timestamp_to_utc

def upload_processed_df(processed_dataframes: dict[str, pd.DataFrame], 
                        counters_dates: dict[str, pd.DataFrame], 
                        s3: boto3.client, 
                        logger: logging.Logger, processed_bucket: str) -> None:
    """
    Saves processed dataframes in .parquet format in /tmp folder and uploads them to S3 processed bucket, determining the path using processed tablenames, plus latest counter and timestamp read from the corresponding tables in the ingestion bucket.
    The map between ingested and processed tables is contained in the dictionary "old_to_new_tables".

    Args:
        processed_dataframes (Dict[str, Any]): Dictionary containing processed dataframes.
        counters_dates (Dict[str, Any]): Dictionary containing latest counters and timestamps read from the ingestion bucket.
        s3 (boto3.client): Boto3 client for S3.
        logger (logging.Logger): Logger object for logging.
        processed_bucket: the name of the aws s3 processed bucket.

    Returns:
        None
    """    
    old_to_new_tables={'fact_sales_order':'sales_order', 'dim_date':'sales_order','dim_staff':'staff', 'dim_currency':'currency','dim_design':'design',
                       'dim_transaction':'transaction','dim_payment_type':'payment_type','fact_purchase_order':'purchase_order','fact_payment':'payment', 'dim_counterparty':'counterparty', 'dim_location':'sales_order'}
    for tablename in processed_dataframes.keys():
        # get method is necessary if one or more tables are not getting updated. In this case, we pass a dummy counter and date to path_to_parquet, but hopefully no file should be uploaded to the s3 bucket
        path=path_to_parquet(tablename, counters_dates.get(old_to_new_tables[tablename],[0,'2022-11-03 14:20:49.962'])[0], convert_sql_timestamp_to_utc(counters_dates.get(old_to_new_tables[tablename],[0,'2022-11-03 14:20:49.962'])[1]))
        folder_name = Path(f"/tmp/{tablename}").mkdir(parents=True, exist_ok=True)
        processed_dataframes[tablename].to_parquet(f'/tmp/{path}',index=False) 
        try:
            s3.upload_file(Filename=f"/tmp/{path}", Bucket=processed_bucket, Key=path)
        except FileNotFoundError:
            tab_name = path.split("/")[0]
            logger.info(f"No rows added or modified to table {tab_name}")
