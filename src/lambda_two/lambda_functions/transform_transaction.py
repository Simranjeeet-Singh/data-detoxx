import pandas as pd


def dim_transaction(df_transaction: pd.DataFrame):
    """
    This function performs data tranformation on transaction table in our original database and converts it into
    dim_transaction table as required in our final schema.

    Input:
    df_transaction (pd.DataFrame)-> The original table in dataframe

    Output:
    final_transaction (pd.DataFrame)-> The final table in data warehouse schema
    """

    try:
        final_transaction = pd.DataFrame()
        for field in df_transaction.columns.to_list():
            if field in [
                "transaction_id",
                "transaction_type",
                "sales_order_id",
                "purchase_order_id",
            ]:
                final_transaction[field] = df_transaction[field].copy()
        final_transaction.fillna({"sales_order_id": 0}, inplace=True)
        final_transaction.fillna({"purchase_order_id": 0}, inplace=True)
        final_transaction['sales_order_id']=final_transaction['sales_order_id'].astype("int64")
        final_transaction['purchase_order_id']=final_transaction['purchase_order_id'].astype("int64")
        return final_transaction
    except Exception as e:
        raise e
