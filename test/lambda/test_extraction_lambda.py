from src.lambda_one.lambda_functions.extraction_lambda import (
    extract_tablenames,
    save_table_to_csv,
    path_to_csv,
    extract_last_updated_from_table,
)
from unittest.mock import patch, Mock, MagicMock
import datetime
import pandas as pd


def test_import_works():
    assert True


def test_extract_tablenames_one_table():
    """
    extract_tablenames extracts names from db with one table
    """
    with patch(
        "src.lambda_code.lambda_functions.extraction_lambda.Connection"
    ) as conn_patched:
        conn_patched.run.return_value = [["ciao"]]
        assert extract_tablenames(conn_patched) == ["ciao"]


def test_extract_tablenames_zero_tables():
    """
    extract_tablenames extracts names from db with zero tables
    """
    with patch(
        "src.lambda_code.lambda_functions.extraction_lambda.Connection"
    ) as conn_patched:
        conn_patched.run.return_value = []
        assert extract_tablenames(conn_patched) == []


def test_extract_tablenames_many_tables():
    """
    extract_tablenames extracts names from db with many tables,
    including a "_prisma_migrations" that should not be extracted
    """
    with patch(
        "src.lambda_code.lambda_functions.extraction_lambda.Connection"
    ) as conn_patched:
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
    assert path_to_csv("table", 0, "2010") == "table/table__[#0]__2010.csv"
    assert (
        path_to_csv("table2", 10, "2010-10-10")
        == "table2/table2__[#10]__2010-10-10.csv"
    )
    assert (
        path_to_csv("table10", 100000, "2010-10-T10101010100Z")
        == "table10/table10__[#100000]__2010-10-T10101010100Z.csv"
    )


def test_extract_last_timestamp():
    """
    extract_last_date retrieves the only entry of a single row
    """
    with patch(
        "src.lambda_code.lambda_functions.extraction_lambda.Connection"
    ) as conn_patched:
        conn_patched.run.return_value = [
            [datetime.datetime(2022, 11, 3, 14, 20, 52, 18600)]
        ]
        assert extract_last_updated_from_table(
            conn_patched, "table"
        ) == datetime.datetime(2022, 11, 3, 14, 20, 52, 18600)


def test_save_table_to_csv_one_row():
    """
    Check that save_table_to_csv calls pd dataframe and passes it the rows - one row case
    """
    with patch("pandas.DataFrame") as df_mock:
        rows = [
            [
                "data1",
                "data2",
                "data3",
                datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
            ]
        ]
        save_table_to_csv(
            [
                {"name": "1"},
                {"name": 2},
                {"name": 3},
                {"name": "last_updated"},
            ],
            rows,
            "path",
            Mock(),
        )
        df_mock.assert_called_once_with(rows)


def test_save_table_to_csv_three_rows():
    """
    Check that save_table_to_csv calls pd dataframe and passes it the rows - three rows case
    """
    with patch("pandas.DataFrame") as df_mock:
        rows = [
            [
                "data1",
                "data2",
                "data3",
                datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
            ],
            [
                "data1",
                "data2",
                "data3",
                datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
            ],
            [
                "data1",
                "data2",
                "data3",
                datetime.datetime(2022, 11, 3, 14, 20, 52, 18600),
            ],
        ]
        save_table_to_csv(
            [
                {"name": "1"},
                {"name": 2},
                {"name": 3},
                {"name": "last_updated"},
            ],
            rows,
            "path",
            Mock(),
        )
        df_mock.assert_called_once_with(rows)


def test_save_table_to_csv_no_rows():
    """
    Check that save_table_to_csv doesn't call pd dataframe if there are no rows
    """
    with patch("pandas.DataFrame") as df_mock:
        rows = []
        save_table_to_csv(
            [
                {"name": "1"},
                {"name": 2},
                {"name": 3},
                {"name": "last_updated"},
            ],
            rows,
            "path",
            Mock(),
        )
        df_mock.assert_not_called()
