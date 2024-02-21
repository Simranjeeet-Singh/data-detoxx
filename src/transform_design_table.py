import pandas as pd


def transform_design_table(design_df: pd.DataFrame) -> pd.DataFrame:
    """
    Simplify a design table DataFrame by selecting specific columns of interest.

    This function filters the input DataFrame to include only the columns related to design ID, design name, file location, and file name.

    Parameters:
    - design_df (pd.DataFrame): A DataFrame containing design-related data, expected to have at least the columns 'design_id', 'design_name', 'file_location', and 'file_name'.

    Returns:
    - pd.DataFrame: A new DataFrame that includes only the 'design_id', 'design_name', 'file_location', and 'file_name' columns from the original DataFrame.
    """
    transformed_df = design_df[[
        "design_id", "design_name", "file_location", "file_name"]]

    return transformed_df
