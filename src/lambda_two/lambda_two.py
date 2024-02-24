import logging
import boto3
import pandas as pd
from utils.file_reading_utils import list_files_from_s3, get_dataframe_from_s3, return_latest_counter_and_timestamp_from_filenames, path_to_parquet
from utils.date_utils import convert_sql_timestamp_to_utc
from pathlib import Path

# Transformer functions
from lambda_functions.fact_sales_transform import fact_sales_transformer
from lambda_functions.transform_date_table import transform_date_table
from lambda_functions.transform_counterparty import dim_counterparty
from lambda_functions.transform_staff_table import transform_staff_table
from lambda_functions.transform_currency_table import transform_currency_table
from lambda_functions.transform_design_table import transform_design_table
from lambda_functions.transform_location_table import transform_location_table
from lambda_functions.transform_transaction import dim_transaction
from lambda_functions.transform_payment_type import dim_payment_type
from lambda_functions.transform_fact_purchase_order import transform_fact_purchase_order
from lambda_functions.transform_fact_payment import fact_payment

INGESTION_BUCKET='data-detox-ingestion-bucket'

def lambda_handler2(event, context):
    try:
        s3 = boto3.client("s3")
        logger = logging.getLogger("MyLogger")
        logger.setLevel(logging.INFO)
        tables_ingestion=list_files_from_s3(INGESTION_BUCKET)
        tablenames_ingestion=list(set([element.split('__')[0] for element in tables_ingestion ]))
        dataframes,counters_dates={},{}
        non_updating_tables=['department', 'counterparty', 'currency', 'payment_type', 'address']
        for tablename in tablenames_ingestion:
            if tablename in non_updating_tables:
                df=get_dataframe_from_s3(INGESTION_BUCKET,tablename)
                tb_counters_dates=(1,'2022-11-03 14:20:51.563') #hardcoded random date
            else:
                tablename_files=[element for element in tables_ingestion if element.split('__')[0]==tablename]
                tb_counters_dates=return_latest_counter_and_timestamp_from_filenames(tablename,tablename_files)
                df=get_dataframe_from_s3(INGESTION_BUCKET,tablename, counter_start=tb_counters_dates[0])
            dataframes[tablename]=df
            counters_dates[tablename]=tb_counters_dates
        #dataframes is a dictionary containining all dataframes with the last updated/added data
        #counters_dates is a dictionary containining corresponding counters and latest dates
        processed_dataframes=process_dataframes(dataframes)
        old_to_new_tables={'fact_sales_order':'sales_order', 'dim_date':'sales_order','dim_staff':'staff', 'dim_currency':'currency','dim_design':'design',
                       'dim_transaction':'transaction','dim_payment_type':'payment_type','fact_purchase_order':'purchase_order','fact_payment':'payment', 'dim_counterparty':'counterparty', 'dim_location':'sales_order'}
        for tablename in processed_dataframes.keys():
            path=path_to_parquet(tablename, counters_dates[old_to_new_tables[tablename]][0], convert_sql_timestamp_to_utc(counters_dates[old_to_new_tables[tablename]][1]))
            folder_name = Path(f"/tmp/{tablename}").mkdir(parents=True, exist_ok=True)
            processed_dataframes[tablename].to_parquet('/tmp/'+path,index=False) 
            try:
                s3.upload_file(Filename=f"/tmp/{path}", Bucket='data-detox-processed-bucket', Key=path)
            except FileNotFoundError:
                tab_name = path.split("__")[0]
                logger.info(f"No rows added or modified to table {tab_name}")
    except Exception as e:
        logger.error(e)
        raise RuntimeError

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
    processed_df_dict['fact_sales_order']=fact_sales_transformer(dataframes['sales_order'], 1) # Second passed arguement to be confirmed
    processed_df_dict['dim_date']=transform_date_table(dataframes['sales_order'])
    # processed_df_dict['dim_counterparty']=dim_counterparty(dataframes['counterparty'], dataframes['address'])
    #bugged
    processed_df_dict['dim_staff']=transform_staff_table(dataframes['staff'], dataframes['department'])
    processed_df_dict['dim_currency']=transform_currency_table(dataframes['currency'])
    processed_df_dict['dim_design']=transform_design_table(dataframes['design'])
    # processed_df_dict['dim_location']=transform_location_table(dataframes['location'])
    # there's no table location in original db, fix this
    processed_df_dict['dim_transaction']=dim_transaction(dataframes['transaction'])
    processed_df_dict['dim_payment_type']=dim_payment_type(dataframes['payment_type'])
    processed_df_dict['fact_purchase_order']=transform_fact_purchase_order(dataframes['purchase_order'])
    processed_df_dict['fact_payment']=fact_payment(dataframes['payment'])

    return processed_df_dict

if __name__=='__main__':
    lambda_handler2('test','test')

