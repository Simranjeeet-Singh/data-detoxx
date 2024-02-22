from src.extract_date import extract_date

import pandas as pd


def transform_date_table(sales_order_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a DataFrame containing sales order data by extracting and 
    structuring date information from specified date columns. 

    Parameters:
    - `sales_order_df`: The input DataFrame containing sales order data with multiple date-related columns.

    Returns:
    - `pd.DataFrame`: A new DataFrame where each row corresponds to a unique date extracted from the input DataFrame.
    """

    date_df = pd.DataFrame([])

    columns_of_interest = ['created_at', 'last_updated',
                           'agreed_delivery_date', 'agreed_payment_date']

    columns_to_process = [
        col for col in columns_of_interest if col in sales_order_df.columns]

    melted_df = pd.melt(
        sales_order_df, value_vars=columns_to_process, value_name='date')

    date_df[['date_id', 'year', 'month', 'day', 'day_of_week',
            'day_name', 'month_name', 'quarter']] = melted_df['date'].apply(
        lambda x: pd.Series(extract_date(x)))

    return date_df.drop_duplicates()
