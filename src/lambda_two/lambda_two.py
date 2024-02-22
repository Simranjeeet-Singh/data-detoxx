import logging
import boto3
#TBD: import all transformation functions

def lambda_handler2(event, context):
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    tablenames=list_tablenames_from_s3('data-detox-ingestion-bucket')
    dataframes={}
    for tablename in tablenames:
        df='' #john_function('data-detox-ingestion-bucket', tablename)
        dataframes[tablename]=df
    #dataframes is a dictionary containining all dataframes with the last updated/added data 
    process_dataframes(dataframes)
    
def list_tablenames_from_s3(bucket_name: str) -> list[str]:
    """
    Args : bucket_name as a `string` \n
    Returns : list of table names inside the bucket as `list` of `strings`
    """
    client = boto3.client("s3")
    response = client.list_objects(Bucket=bucket_name)
    if "Contents" not in response:
        return []
    return list(set([item["Key"].split('/')[0] for item in response["Contents"]]))

def process_dataframes(dataframes):
    df_fact_sales_order=utils_fact_sales_order(df_sales_order)

    df_dim_date=utils_dim_date(df_sales_order) #needs date_expander util

    df_dim_counterparty=utils_dim_counterparty(df_counterparty)

    df_dim_staff=utils_dim_staff(df_staff,df_department)

    df_dim_currency=utils_dim_currency(df_currency) #needs currency code converter util

    df_dim_desing=utils_dim_design(df_design)

    df_dim_location=utils_dim_location(df_address)