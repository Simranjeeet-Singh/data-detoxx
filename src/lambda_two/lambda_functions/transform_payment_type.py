import pandas as pd


def dim_payment_type(df_payment_type: pd.DataFrame):
    """
    This function performs data tranformation on payment_type table in our original database and converts it into
    dim payment_type table as required in our final schema.

    Input:
    df_payment (pd.DataFrame)-> The original table in dataframe

    Output:
    final_payment_type (pd.DataFrame)-> The final table in data warehouse schema
    """
    try:
        final_payment_type = pd.DataFrame()
        for field in df_payment_type.columns.to_list():
            if field in ["payment_type_id", "payment_type_name"]:
                final_payment_type[field] = df_payment_type[field].copy()

        return final_payment_type
    except Exception as e:
        raise e
