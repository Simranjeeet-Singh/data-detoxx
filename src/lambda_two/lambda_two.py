import logging
import boto3
import pandas as pd
from utils.file_reading_utils import list_files_from_s3
from lambda_functions.path_to_parquet import path_to_parquet

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

def lambda_handler2(event, context):
    try:
        s3 = boto3.client("s3")
        logger = logging.getLogger("MyLogger")
        logger.setLevel(logging.INFO)
        tablenames=list(set([element.split('__')[0] for element in list_files_from_s3('data-detox-processed-bucket')]))
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
            #save each df tlo appropriate parquet file in tmp with good name
            #path structure is 'tablename/tablename__[#version]__date_last_updated.parquet'
            #find_path should generate it
            path=path_to_parquet(tablename, 1, 'Date') # TODO - change attributes passed into function 
            process_dataframes[tablename].to_parquet('/tmp/'+path,index=False)
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
    processed_df_dict['dim_counterparty']=dim_counterparty(dataframes['counterparty'], dataframes['address'])
    processed_df_dict['dim_staff']=transform_staff_table(dataframes['staff'], dataframes['department'])
    processed_df_dict['dim_currency']=transform_currency_table(dataframes['currency'])
    processed_df_dict['dim_design']=transform_design_table(dataframes['design'])
    processed_df_dict['dim_location']=transform_location_table(dataframes['location'])
    processed_df_dict['dim_transaction']=dim_transaction(dataframes['transaction'])
    processed_df_dict['dim_payment_type']=dim_payment_type(dataframes['payment_type'])
    processed_df_dict['fact_purchase_order']=transform_fact_purchase_order(dataframes['purchase_order'])
    processed_df_dict['fact_payment']=fact_payment(dataframes['payment'])

    return processed_df_dict

# if __name__=='__main__':
#     lambda_handler2('test','test')

