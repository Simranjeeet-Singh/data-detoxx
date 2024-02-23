import logging
import boto3
import pandas as pd
#TBD: import all transformation functions

def lambda_handler2(event, context):
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    tablenames=list_tablenames_from_s3('data-detox-ingestion-bucket')
    dataframes={}
    for tablename in tablenames:
        if tablename=='department' or tablename=='counterparty':
            df=''#read all csvs for that table
        else:
            df='' #read only last updates via john_function('data-detox-ingestion-bucket', tablename)
            dataframes[tablename]=df
    #dataframes is a dictionary containining all dataframes with the last updated/added data 
    processed_dataframes=process_dataframes(dataframes)
    for tablename in process_dataframes.keys():
        #save each df to appropriate parquet file in tmp with good name
        #path structure is 'tablename/tablename__[#version]__date_last_updated.parquet'
        #find_path should generate it
        path=find_path(tablename)
        process_dataframes[tablename].to_parquet('/tmp/'+path)
    #upload tmp to the processed bucket
    #to be written
    
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


def process_dataframes(dataframes: dict[pd.DataFrame]) -> dict[pd.DataFrame]:
    """
    Process a dictionary of pandas dataframes representing all tables in the original database.
    
    Args:
    - dataframes (Dict[str, pd.DataFrame]): A dictionary where keys represent table names and values are the corresponding pandas dataframes.
    
    Returns:
    - processed_df_dict (Dict[str, pd.DataFrame]): A dictionary containing processed pandas dataframes with keys being the process table names.
    
    The function processes each dataframe using our transformation functions and stores them in a dictionary.
    The keys of the resulting dictionary correspond to the processed table names, and the values are the processed dataframes.
    The processed table names are: 'fact_sales_order', 'dim_date', 'dim_counterparty', 'dim_staff', 'dim_currency',
    'dim_design', and 'dim_location'.
    """
    processed_df_dict={}

    #transform_ functions need to be replaced with our actual transformation functions
    processed_df_dict['fact_sales_order']=transform_fact_sales_order(dataframes['sales_order'])
    processed_df_dict['dim_date']=transform_dim_date(dataframes['sales_order'])
    processed_df_dict['dim_counterparty']=transform_fact_sales_order(dataframes['counterparty'],dataframes['address'])
    processed_df_dict['dim_staff']=transform_fact_sales_order(dataframes['staff'],dataframes['department'])
    processed_df_dict['dim_currency']=transform_fact_sales_order(dataframes['currency'])
    processed_df_dict['dim_design']=transform_fact_sales_order(dataframes['design'])
    processed_df_dict['dim_location']=transform_fact_sales_order(dataframes['location'])
    #add more transformations here if we go beyond MVP
    return processed_df_dict

def find_path(tablename):
    #to be written
    pass

print(get_secret())