from src.lambda_functions.extraction_lambda import (
    extract_tablenames,
    save_table_to_csv,
    save_db_to_csv,
    convert_to_utc,
    path_to_csv,
    extract_last_updated_from_table,
    save_rows_to_csv,
)
from unittest.mock import patch, Mock
import datetime
import pandas as pd


# Some of these tests are now broken, due to change in main functions. Don't run them yet
def test_import_works():
    assert True


def test_extract_tablenames_one_table():
    """
    extract_tablenames extracts names from db with one table
    """
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value = [["ciao"]]
        assert extract_tablenames(conn_patched) == ["ciao"]


def test_extract_tablenames_zero_tables():
    """
    extract_tablenames extracts names from db with zero tables
    """
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value = []
        assert extract_tablenames(conn_patched) == []


def test_extract_tablenames_many_tables():
    """
    extract_tablenames extracts names from db with many tables,
    including a "_prisma_migrations" that should not be extracted
    """
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value = [
            ["a"],
            ["b"],
            ["c"],
            ["d"],
            ["e"],
            ["_prisma_migrations"],
            ["f"],
        ]
        assert extract_tablenames(conn_patched) == ["a", "b", "c", "d", "e", "f"]


def test_path_to_csv():
    """
    path_to_csv formats the path in the intended way
    """
    assert path_to_csv("table", 0, "2010") == "./table/table_[#0]_2010.csv"
    assert (
        path_to_csv("table2", 10, "2010-10-10")
        == "./table2/table2_[#10]_2010-10-10.csv"
    )
    assert (
        path_to_csv("table10", 100000, "2010-10-T10101010100Z")
        == "./table10/table10_[#100000]_2010-10-T10101010100Z.csv"
    )


def test_extract_last_timestamp():
    """
    extract_last_date retrieves the only entry of a single row
    """
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value = [
            [datetime.datetime(2022, 11, 3, 14, 20, 52, 18600)]
        ]
        assert extract_last_updated_from_table(
            conn_patched, "table"
        ) == datetime.datetime(2022, 11, 3, 14, 20, 52, 18600)


def test_save_table_to_csv_one_row():
    """
    Check that save_table_to_csv calls the function save_rows_to_csv once with the correct arguments
    (rows, column_names, path_csv), when we only have a single row
    """
    with patch("src.lambda_functions.extraction_lambda.convert_to_utc") as date_patched:
        date_patched.return_value = "random"
        with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
            conn_patched.run.return_value = [
                [
                    "data1",
                    "data2",
                    "data3",
                    datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
                ]
            ]
            conn_patched.columns = [
                {"name": "1"},
                {"name": 2},
                {"name": 3},
                {"name": "last_updated"},
            ]
            with patch(
                "src.lambda_functions.extraction_lambda.path_to_csv"
            ) as path_patched:
                path_patched.return_value = "random"
                with patch(
                    "src.lambda_functions.extraction_lambda.save_rows_to_csv"
                ) as save_patched:
                    save_table_to_csv(
                        conn_patched,
                        "random",
                        datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
                        0,
                    )
                    save_patched.assert_called_once_with(
                        ["1", 2, 3, "last_updated"], conn_patched.run(), path_patched()
                    )


def test_save_table_to_csv_multiple_rows():
    with patch("src.lambda_functions.extraction_lambda.convert_to_utc") as date_patched:
        date_patched.return_value = "random"
        with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
            conn_patched.run.return_value = [
                [
                    "data1",
                    "data2",
                    "data3",
                    datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
                ],
                [
                    "data",
                    "data",
                    "data",
                    datetime.datetime(2023, 11, 3, 14, 20, 52, 18600),
                ],
                [
                    "datar",
                    "datar",
                    "datar",
                    datetime.datetime(2024, 11, 3, 14, 20, 52, 18600),
                ],
                [
                    "data5",
                    "data5",
                    "data5",
                    datetime.datetime(2025, 11, 3, 14, 20, 52, 18600),
                ],
                [
                    "data1",
                    "data2",
                    "data3",
                    datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
                ],
            ]
            conn_patched.columns = [
                {"name": "1"},
                {"name": 2},
                {"name": 3},
                {"name": "last_updated"},
            ]
            with patch(
                "src.lambda_functions.extraction_lambda.path_to_csv"
            ) as path_patched:
                path_patched.return_value = "random"
                with patch(
                    "src.lambda_functions.extraction_lambda.save_rows_to_csv"
                ) as save_patched:
                    save_table_to_csv(
                        conn_patched,
                        "random",
                        datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
                        0,
                    )
                    save_patched.assert_called_once_with(
                        ["1", 2, 3, "last_updated"], conn_patched.run(), path_patched()
                    )


def test_save_table_to_csv_one_row():
    """
    check that if rows are non-empty, pd.DataFrame gets called once and passed the rows
    """
    with patch("pandas.DataFrame") as df_mock:
        rows = [[1, 2, 3], [1, 2, 3]]
        cols_name = ["a", "b", "c"]
        path = "path"
        save_rows_to_csv(cols_name, rows, path)
        df_mock.assert_called_once_with(rows)


def test_save_table_to_csv_zero_rows():
    """
    check that if rows are empty, pd.DataFrame does not get called
    """
    with patch("pandas.DataFrame") as df_mock:
        rows = []
        cols_name = ["a", "b", "c"]
        path = "path"
        save_rows_to_csv(cols_name, rows, path)
        df_mock.assert_not_called()


# missing save to db test
# probably should complete the function first
