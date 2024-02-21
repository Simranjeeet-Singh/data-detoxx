import pandas as pd

from src.currency_code_to_currency_name import currency_code_to_currency_name as cccn


def transform_currency_table(currency_df: pd.DataFrame) -> pd.DataFrame:
    currency_df['currency_name'] = currency_df['currency_code'].apply(cccn)
    transformed_df = currency_df[[
        'currency_id', 'currency_code', 'currency_name']]
    return transformed_df
