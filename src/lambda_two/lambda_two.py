import logging
import boto3
import pandas as pd
from utils.file_reading_utils import list_files_from_s3, get_dataframe_from_s3, return_latest_counter_and_timestamp_from_filenames, tables_reader_from_s3
from utils.date_utils import convert_sql_timestamp_to_utc
from pathlib import Path
from utils.state_file import write_state_file

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
from lambda_functions.upload_processed_df import upload_processed_df

INGESTION_BUCKET='data-detox-ingestion-bucket'
PROCESSED_BUCKET='data-detox-processed-bucket'


def lambda_handler2(event, context):
    try:
        s3 = boto3.client("s3")
        logger = logging.getLogger("MyLogger")
        logger.setLevel(logging.INFO)
        all_files_from_ingestion=list_files_from_s3(INGESTION_BUCKET)
        dataframes, counters_dates=tables_reader_from_s3(all_files_from_ingestion, INGESTION_BUCKET)
        #dataframes is a dictionary containining all dataframes with the last updated/added data
        #counters_dates is a dictionary containining corresponding counters and latest dates
        processed_dataframes, state_file_dict=process_dataframes(dataframes)
        upload_processed_df(processed_dataframes, counters_dates, s3, logger, PROCESSED_BUCKET)
        write_state_file('/tmp/state_file.json', state_file_dict)
        s3.upload_file(Filename=f"/tmp/state_file.json", Bucket=PROCESSED_BUCKET, Key='state_file.json')
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
    - state_file_dict (Dict[str, bool]): A dictionary containing whether a given table has received updates.
    
    The function processes each dataframe using our transformation functions and stores them in a dictionary.
    The keys of the resulting dictionary correspond to the processed table names, and the values are the processed dataframes.
    The processed table names are: 'fact_sales_order', 'dim_date', 'dim_counterparty', 'dim_staff', 'dim_currency',
    'dim_design', and 'dim_location'.
    """
    processed_df_dict={}
    state_file_dict={'fact_sales_order':False, 'dim_date':False, 'dim_staff':False, 'dim_design':False, 'dim_transaction':False, 'fact_purchase_order':False, 'fact_payment':False, 'dim_payment_type':True, 'dim_currency':True, 'dim_counterparty':True, 'dim_location':True}
    try:
        if 'sales_order' in dataframes:
            processed_df_dict['fact_sales_order']=fact_sales_transformer(dataframes['sales_order'])
            processed_df_dict['dim_date']=transform_date_table(dataframes['sales_order']) 
            state_file_dict['fact_sales_order']=True
            state_file_dict['dim_date']=True
        if 'staff' in dataframes:
            processed_df_dict['dim_staff']=transform_staff_table(dataframes['staff'], dataframes['department'])
            state_file_dict['dim_staff']=True
        if 'design' in dataframes:
            processed_df_dict['dim_design']=transform_design_table(dataframes['design'])
            state_file_dict['dim_design']=True
        if 'transaction' in dataframes:
            processed_df_dict['dim_transaction']=dim_transaction(dataframes['transaction']) 
            state_file_dict['dim_transaction']=True
        if 'purchase_order' in dataframes:
            processed_df_dict['fact_purchase_order']=transform_fact_purchase_order(dataframes['purchase_order'])
            state_file_dict['fact_purchase_order']=True
        if 'payment' in dataframes:
            processed_df_dict['fact_payment']=fact_payment(dataframes['payment'])
            state_file_dict['fact_payment']=True
        # these are always non-empty
        processed_df_dict['dim_payment_type']=dim_payment_type(dataframes['payment_type'])
        processed_df_dict['dim_currency']=transform_currency_table(dataframes['currency'])
        processed_df_dict['dim_counterparty']=dim_counterparty(dataframes['counterparty'], dataframes['address'])
        processed_df_dict['dim_location']=transform_location_table(dataframes['address'])

    except Exception as e:
        raise RuntimeError
    return processed_df_dict, state_file_dict

if __name__=='__main__':
    lambda_handler2('test','test')

