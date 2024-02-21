import pandas as pd
from datetime import datetime
def sales_dt_transform(datetime : datetime) -> tuple[str,str]:
    'converts datetime to date and time (psql format)'
    return 'a','b'

def precision_changer(number : float) -> float:
    '''
    returns number to numerical precision of 10,2
    '''

def fact_sales_transformer(df_sales_order : pd.DataFrame) -> pd.DataFrame:
    '''
    
    '''
    sales_col=df_sales_order['created_at'].apply(lambda x: pd.Series(sales_dt_transform(x),index=['created_date', 'created_time']))
    # df_sales_order['last_updated'].apply(sales_dt_transform,result_type='expand')
    # created_date, created_time = [sales_dt_transform(element) for element in df_sales_order['created_at'].values]
    # last_updated_date, last_updated_time = [sales_dt_transform(element) for element in df_sales_order['last_updated'].values]
    # unit_price = [precision_changer(element) for element in df_sales_order['unit_price']]
    # agreed_payment_date=[str_to_date(element) for element in df_sales_order['agreed_payment_date']]
    # agreed_delivery_date=[str_to_date(element) for element in df_sales_order['agreed_delivery_date']]
    df_fact_sales=df_sales_order[['sales_order_id','staff_id','counterparty_id','units_sold','currency_id','design_id','agreed_delivery_location']]
    df_fact_sales.insert(0,'sales_record_id',range(1,1+len(df_fact_sales)))
    df_fact_sales.index=df_fact_sales.loc[:,'sales_record_id'].values
    df_fact_sales
    return df_fact_sales
    
if __name__== '__main__':
    df=pd.DataFrame([{'sales_order_id':1, 'staff_id':1, 'created_at': 1, 'counterparty_id':1, 'units_sold':1,'currency_id':1,'design_id':1,'agreed_delivery_location':1},{'sales_order_id':1, 'staff_id':1, 'created_at': 1, 'counterparty_id':1, 'units_sold':1,'currency_id':1,'design_id':1,'agreed_delivery_location':1}])
    print(fact_sales_transformer(df)[1])