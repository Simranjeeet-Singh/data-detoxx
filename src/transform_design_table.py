import pandas as pd


def transform_design_table(design_df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = design_df[[
        "design_id", "design_name", "file_location", "file_name"]]

    return transformed_df
