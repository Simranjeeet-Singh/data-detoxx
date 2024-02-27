import pandas as pd
from utils.currency_code_to_currency_name import (
    currency_code_to_currency_name as cccn,
)
from datetime import datetime


def currency_dt_transform(datetime_str : str) -> tuple[str,str]:
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

def transform_currency_table(currency_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform a DataFrame containing currency codes by adding a column with the corresponding currency names.

    This function takes a DataFrame that includes a column 'currency_code', applies a conversion function (assumed to be named `cccn`) to each currency code to obtain its corresponding currency name, and then constructs a new DataFrame that includes the original 'currency_id' and 'currency_code' columns along with the newly added 'currency_name' column.

    Parameters:
    - currency_df (pd.DataFrame): A DataFrame with at least the following columns:
        - 'currency_code': Column containing currency codes (ISO 4217 format).
        - 'currency_id': An identifier for each currency entry.

    Returns:
    - pd.DataFrame: A new DataFrame based on the input but with an additional 'currency_name' column, containing the names corresponding to the currency codes.

    Example:
    Assuming `currency_df` is a DataFrame with columns ['currency_id', 'currency_code'] like below:
    | currency_id | currency_code |
    |-------------|---------------|
    |           1 | EUR           |
    |           2 | USD           |

    The output will be a DataFrame with an additional 'currency_name' column:
    | currency_id | currency_code | currency_name         |
    |-------------|---------------|-----------------------|
    |           1 | EUR           | Euro                  |
    |           2 | USD           | United States dollar  |

    Note:
    - The function `cccn` used for converting currency codes to currency names is assumed to be defined elsewhere.
    """
    currency_df["currency_name"] = currency_df["currency_code"].apply(cccn)
    updated_cols=currency_df['last_updated'].apply(lambda x: pd.Series(currency_dt_transform(x),index=['last_updated_date', 'last_updated_time']))
    currency_df=currency_df.join([updated_cols])
    transformed_df = currency_df[["currency_id", "currency_code", "currency_name",'last_updated_date','last_updated_time']]

    return transformed_df
