import pandas as pd
import math 
from datetime import datetime
def fact_payment(df_payment:pd.DataFrame):
    """
    This function performs data tranformation on transaction table in our original database and converts it into
    dim_transaction table as required in our final schema.
    
    Input:
    df_payment (pd.DataFrame)-> The original table in dataframe

    Output:
    final_payment (pd.DataFrame)-> The final table in data warehouse schema
    """
    try:
        #The unique serial id needs to be fixed to only start the counter where it left off after the updated batch of data is passed on by lambda 2.
        final_payement=pd.DataFrame()
        for field in df_payment.columns.to_list():
            if field in ['created_at']:
                date_time=df_payment['created_at'].apply(lambda x: pd.Series(sales_dt_transform(x)))
                final_payement['created_date']=date_time[0]
                final_payement['created_time']=date_time[1]
                
            elif field in ['last_updated']:
                date_time=df_payment['created_at'].apply(lambda x: pd.Series(sales_dt_transform(x)))
                final_payement['last_updated_date']=date_time[0]
                final_payement['last_updated_time']=date_time[1]
            elif field in ['payment_id','transaction_id','counterparty_id','payment_amount','currency_id','payment_type_id',
                           'paid','payment_date','company_ac_number','counterparty_ac_number']:
                final_payement[field]=df_payment[field].copy()
        return final_payement
            
    except Exception as e:
        raise e
    
                
    


def sales_dt_transform(timestamp_str : str) -> tuple[str,str]:
    """
    Converts datetime to date and time.

    Args:
        datetime_str (str): A string representing the datetime in the format 'YYYY-MM-DD HH:MM:SS.sss'.

    Returns:
        tuple[str, str]: A tuple of two strings representing the date and time components.
    """
    timestamp=datetime.fromisoformat(timestamp_str)
    date=timestamp.date()
    time=timestamp.time()
    return str(date), str(time)