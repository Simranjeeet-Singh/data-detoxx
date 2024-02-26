import pandas as pd
from datetime import datetime

def sales_dt_transform(datetime_str : str) -> tuple[str,str]:
    """
    Converts datetime to date and time.

    Args:
        datetime_str (str): A string representing the datetime in the format 'YYYY-MM-DD HH:MM:SS.sss'.

    Returns:
        tuple[str, str]: A tuple of two strings representing the date and time components.
    """
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        # If milliseconds are missing, append '.000' to the string
        datetime_str += '.000'
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    return str(dt.date()), str(dt.time())

def precision_changer(num : float) -> float:
    '''
    Change the precision of a float number to 8 integer and 2 decimal digits.

    Parameters:
        num (float): The number to be changed.

    Returns:
        float: The number with precision of 10,2.
    '''
    [integer, decimal]=('{:.2f}'.format(num)).split('.')
    if int(integer)>99999999:
        integer=99999999
    return float(f'{integer}.{decimal}')

def fact_sales_transformer(df_sales_order : pd.DataFrame, last_serial_key: int) -> pd.DataFrame:
    '''
    This function processes the sales order data DataFrame by performing the following steps:
    1. Extracts and transforms 'created_at' and 'last_updated' columns into separate 'created_date',
       'created_time', 'last_updated_date', and 'last_updated_time' columns.
    2. Applies precision change to the 'unit_price' column.
    3. Selects specific columns from the original DataFrame.
    4. Joins the transformed 'created_cols', 'updated_cols', and 'unit_price' to the selected columns.
    5. Inserts a new column 'sales_record_id' with unique identifiers, starting from last_serial_key.
    6. Sets 'sales_record_id' as the index of the DataFrame.
    7. Renames the 'staff_id' column to 'sales_staff_id'.
    8. Rearranges the columns order as specified.
    '''
    created_cols=df_sales_order['created_at'].apply(lambda x: pd.Series(sales_dt_transform(x),index=['created_date', 'created_time']))
    updated_cols=df_sales_order['last_updated'].apply(lambda x: pd.Series(sales_dt_transform(x),index=['last_updated_date', 'last_updated_time']))
    unit_price = df_sales_order['unit_price'].apply(precision_changer)
    df_fact_sales=df_sales_order[['sales_order_id','staff_id','counterparty_id','units_sold','currency_id','design_id','agreed_delivery_location_id','agreed_payment_date','agreed_delivery_date']]
    df_fact_sales=df_fact_sales.join([created_cols,updated_cols,unit_price])
    df_fact_sales.insert(0,'sales_record_id',range(last_serial_key,last_serial_key+len(df_fact_sales)))
    df_fact_sales.index=df_fact_sales.loc[:,'sales_record_id'].values
    df_fact_sales=df_fact_sales.rename(columns={'staff_id':'sales_staff_id'})
    # Rearrange columns order
    return df_fact_sales[['sales_record_id','sales_order_id','created_date','created_time','last_updated_date','last_updated_time','sales_staff_id','counterparty_id','units_sold','unit_price','currency_id','design_id','agreed_payment_date','agreed_delivery_date','agreed_delivery_location_id']]

if __name__== '__main__':
    df=pd.DataFrame([{'sales_order_id':1, 'staff_id':1, 'created_at': "2022-11-03 14:20:52.186", 'last_updated':"2022-11-03 14:20:52.186",'counterparty_id':1, 'units_sold':1,'currency_id':1,'design_id':1,'agreed_delivery_location_id':1,'unit_price':1,'agreed_delivery_date':1,'agreed_payment_date':1},{'agreed_delivery_date':1,'agreed_payment_date':1,'sales_order_id':1,'last_updated':"2022-11-03 14:20:52.186", 'staff_id':1, 'created_at': "2022-11-03 14:20:52.186", 'counterparty_id':1, 'units_sold':1,'currency_id':1,'design_id':1,'agreed_delivery_location_id':1,'unit_price':1}])
    print(fact_sales_transformer(df).to_markdown())