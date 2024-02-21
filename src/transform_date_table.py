from src.extract_date import extract_date

import pandas as pd


def transform_date_table(sales_order_df: pd.DataFrame) -> pd.DataFrame:
    # from sales_order_df I want to take created_date, laste_updated_date, agreed_delivery_date and agreed_payment_date values and use them as keys in dim_date_table and then use extract_date function to populate the rest of the rows

    # currency_df['currency_name'] = currency_df['currency_code'].apply(cccn)

    date_df = pd.DataFrame([])

    # df[['age', 'gender']] = df['info'].apply(lambda x: pd.Series(extract_values(x)))

    date_df[['date_id', 'year', 'month', 'day', 'day_of_week',
            'day_name', 'month_name', 'quarter']] = sales_order_df['created_date'].apply(
        lambda x: pd.Series(extract_date(x)))
    date_df.loc[len(date_df)] = date_df.loc[0]

    # date_df['date_id'] = sales_order_df['created_date'].apply(extract_date)

    return date_df
# .drop_duplicates()
