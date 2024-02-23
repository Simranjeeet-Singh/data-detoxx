import pandas as pd

from datetime import datetime


def sales_dt_transform(datetime_str: str) -> tuple[str, str]:
    """
    Converts datetime to date and time.

    Args:
        datetime_str (str): A string representing the datetime in the format 'YYYY-MM-DD HH:MM:SS.sss'.

    Returns:
        tuple[str, str]: A tuple of two strings representing the date and time components.
    """
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    return str(dt.date()), str(dt.time())


def transform_fact_purchase_order(purchase_order_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame containing purchase order information, adds a unique 'purchase_record_id' for each row, and reorganizes the DataFrame to include these new columns while maintaining key purchase order details.

    Args:
        purchase_order_df (pd.DataFrame): A DataFrame containing purchase order data

    Returns:
        pd.DataFrame: A transformed DataFrame with the original purchase order details
    """

    created_cols = purchase_order_df['created_at'].apply(lambda x: pd.Series(
        sales_dt_transform(x), index=['created_date', 'created_time']))
    updated_cols = purchase_order_df['last_updated'].apply(lambda x: pd.Series(
        sales_dt_transform(x), index=['last_updated_date', 'last_updated_time']))

    transformed_df = purchase_order_df[['purchase_order_id', 'staff_id',
                                       'counterparty_id', 'item_code', 'item_quantity', 'item_unit_price', 'currency_id', 'agreed_delivery_date', 'agreed_payment_date', 'agreed_delivery_location_id']]

    transformed_df = transformed_df.join([created_cols, updated_cols])

    transformed_df.insert(0, 'purchase_record_id',
                          range(1, 1+len(transformed_df)))
    transformed_df.index = transformed_df.loc[:, 'purchase_record_id'].values

    return transformed_df
