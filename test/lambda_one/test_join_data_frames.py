from src.lambda_two.utils.join_data_frames import left_join_df
from src.lambda_two.utils.join_data_frames import column_filter

import pandas as pd
import pytest


def test_returns_data_frame_as_an_output():
    staff_df = pd.DataFrame([[1, "Jeremie", 2], [2, "Deron", 6], [3, "Jeanette", 6]])
    staff_df.columns = ["staff_id", "name", "department_id"]

    department_df = pd.DataFrame([[6, "Sales", "Manchester"], [2, "HR", "Leeds"]])
    department_df.columns = ["department_id", "department_name", "location"]

    result = left_join_df(staff_df, department_df, "department_id")
    assert type(result) == pd.DataFrame


def test_returns_an_exception_when_passed_with_wrong_data_input():
    with pytest.raises(Exception):
        staff_df = pd.DataFrame([3, "Jeanette", 6])
        staff_df.columns = ["staff_id", "name", "department_id"]

        department_df = pd.DataFrame([[6, "Sales", "Manchester"], [2, "HR", "Leeds"]])
        department_df.columns = ["department_id", "department_name", "location"]

        left_join_df(staff_df, department_df, "department_id")


def test_returns_the_merged_data_frame_with_the_columns_names_of_merged_data_frames():
    staff_df = pd.DataFrame([[1, "Jeremie", 2], [2, "Deron", 6], [3, "Jeanette", 6]])
    staff_df.columns = ["staff_id", "name", "department_id"]

    department_df = pd.DataFrame([[6, "Sales", "Manchester"], [2, "HR", "Leeds"]])
    department_df.columns = ["department_id", "department_name", "location"]

    result = left_join_df(staff_df, department_df, "department_id")
    columns_list = [
        "table1_staff_id",
        "table1_name",
        "table1_department_id",
        "table2_department_id",
        "table2_department_name",
        "table2_location",
    ]

    assert result.columns.to_list() == columns_list


def test_returns_the_merged_data_frame_with_the_columns_names_of_merged_data_frames_when_passed_foreign_key_2():
    staff_df = pd.DataFrame([[1, "Jeremie", 2], [2, "Deron", 6], [3, "Jeanette", 6]])
    staff_df.columns = ["staff_id", "name", "staff_department_id"]

    department_df = pd.DataFrame([[6, "Sales", "Manchester"], [2, "HR", "Leeds"]])
    department_df.columns = ["department_id", "department_name", "location"]

    result = left_join_df(
        staff_df, department_df, "staff_department_id", "department_id"
    )
    columns_list = [
        "table1_staff_id",
        "table1_name",
        "table1_staff_department_id",
        "table2_department_id",
        "table2_department_name",
        "table2_location",
    ]

    assert result.columns.to_list() == columns_list


def test_returns_the_same_table_if_columns_filter_list_is_empty():
    staff_department = pd.DataFrame(
        [
            [1, "Jeremie", 2, 2, "HR", "Leeds"],
            [2, "Deron", 6, 6, "Sales", "Manchester"],
            [3, "Jeanette", 6, 6, "Sales", "Manchester"],
        ]
    )
    staff_department.columns = [
        "staff_id",
        "name",
        "staff_department_id",
        "department_id",
        "department_name",
        "location",
    ]
    result = column_filter(staff_department)
    columns_list = [
        "staff_id",
        "name",
        "staff_department_id",
        "department_id",
        "department_name",
        "location",
    ]
    assert type(result) == pd.DataFrame
    assert result.columns.to_list() == columns_list


def test_returns_the_filtered_table_with_column_names_in_columns_filter_list():
    staff_department = pd.DataFrame(
        [
            [1, "Jeremie", 2, 2, "HR", "Leeds"],
            [2, "Deron", 6, 6, "Sales", "Manchester"],
            [3, "Jeanette", 6, 6, "Sales", "Manchester"],
        ]
    )
    staff_department.columns = [
        "staff_id",
        "name",
        "staff_department_id",
        "department_id",
        "department_name",
        "location",
    ]
    result = column_filter(
        staff_department, ["staff_id", "name", "department_name", "location"]
    )
    columns_list = ["staff_id", "name", "department_name", "location"]
    assert type(result) == pd.DataFrame
    assert result.columns.to_list() == columns_list


def test_returns_the_filtered_table_with_column_names_renamed_in_columns_renamed_list():
    staff_department = pd.DataFrame(
        [
            [1, "Jeremie", 2, 2, "HR", "Leeds"],
            [2, "Deron", 6, 6, "Sales", "Manchester"],
            [3, "Jeanette", 6, 6, "Sales", "Manchester"],
        ]
    )
    staff_department.columns = [
        "staff_id",
        "name",
        "staff_department_id",
        "department_id",
        "department_name",
        "location",
    ]
    result = column_filter(
        staff_department,
        ["staff_id", "name", "staff_department_id", "department_name", "location"],
        ["staff_id", "name", "department_id", "department", "office"],
    )
    columns_list = ["staff_id", "name", "department_id", "department", "office"]
    assert type(result) == pd.DataFrame
    assert result.columns.to_list() == columns_list


def test_raises_an_exception_when_column_filter_contains_wrong_column_name():
    with pytest.raises(Exception):
        staff_department = pd.DataFrame(
            [
                [1, "Jeremie", 2, 2, "HR", "Leeds"],
                [2, "Deron", 6, 6, "Sales", "Manchester"],
                [3, "Jeanette", 6, 6, "Sales", "Manchester"],
            ]
        )
        staff_department.columns = [
            "staff_id",
            "name",
            "staff_department_id",
            "department_id",
            "department_name",
            "location",
        ]
        column_filter(staff_department, ["name", "office"])


def test_raises_a_ValueError_when_columns_renamed_mismatches_columns_filter():
    with pytest.raises(ValueError):
        staff_department = pd.DataFrame(
            [
                [1, "Jeremie", 2, 2, "HR", "Leeds"],
                [2, "Deron", 6, 6, "Sales", "Manchester"],
                [3, "Jeanette", 6, 6, "Sales", "Manchester"],
            ]
        )
        staff_department.columns = [
            "staff_id",
            "name",
            "staff_department_id",
            "department_id",
            "department_name",
            "location",
        ]
        column_filter(staff_department, ["name", "office"], ["staff_name"])
