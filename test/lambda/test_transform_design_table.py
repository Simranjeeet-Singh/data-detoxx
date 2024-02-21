from src.transform_design_table import transform_design_table as tdt
import pandas as pd


def test_all_correct_columns_are_present():

    test_design_df = pd.DataFrame([
        [1, "2023-01-01", "2023-01-02", "Sunrise Landscape",
            "/designs/january/", "sunrise_landscape.png"],
        [2, "2023-02-15", "2023-02-16", "Abstract Art",
            "/designs/february/", "abstract_art.png"],
        [3, "2023-03-10", "2023-03-11", "City Skyline",
            "/designs/march/", "city_skyline.png"],
        [4, "2023-04-05", "2023-04-06", "Mountain Adventure",
            "/designs/april/", "mountain_adventure.png"]
    ])
    test_design_df.columns = [
        "design_id", "created_at", "last_updated", "design_name", "file_location", "file_name"]

    output = tdt(test_design_df)

    assert output.columns.tolist() == [
        "design_id", "design_name", "file_location", "file_name"]


def test_return_type_is_pd_dataframe():
    test_design_df = pd.DataFrame([
        [1, "2023-01-01", "2023-01-02", "Sunrise Landscape",
            "/designs/january/", "sunrise_landscape.png"],
        [2, "2023-02-15", "2023-02-16", "Abstract Art",
            "/designs/february/", "abstract_art.png"],
        [3, "2023-03-10", "2023-03-11", "City Skyline",
            "/designs/march/", "city_skyline.png"],
        [4, "2023-04-05", "2023-04-06", "Mountain Adventure",
            "/designs/april/", "mountain_adventure.png"]
    ])
    test_design_df.columns = [
        "design_id", "created_at", "last_updated", "design_name", "file_location", "file_name"]

    output = tdt(test_design_df)

    assert isinstance(output, pd.DataFrame)
