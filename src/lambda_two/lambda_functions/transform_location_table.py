import pandas as pd


def transform_location_table(location_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a DataFrame of location data by renaming specific columns.

    This function renames the 'address_id' column to 'location_id', and the 'postal_code'
    column to 'postcode'. It then selects a subset of columns relevant for the transformed
    DataFrame.

    Parameters:
    - location_df (pd.DataFrame): The input DataFrame containing location information.

    Returns:
    - pd.DataFrame: A transformed DataFrame with renamed columns and a specific subset of columns.
    """
    transformed_df = location_df.rename(
        columns={'address_id': 'location_id'})
    return transformed_df[['location_id', 'address_line_1', 'address_line_2', 'district', 'city', 'postal_code', 'country', 'phone']]
