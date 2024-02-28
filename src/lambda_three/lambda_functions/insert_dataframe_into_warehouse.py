import pandas as pd
from pg8000.native import Connection, literal, identifier
from pg8000 import exceptions


def insert_dataframes_into_warehouse(
    conn: Connection, dataframes_dict: dict[str, pd.DataFrame]
) -> None:
    """
    Insert data from DataFrames into the warehouse tables.
    Args:
        conn (Connection): The connection object to the PostgreSQL database.
        tables_data (Dict[str, DataFrame]): A dictionary containing table names as keys and DataFrame as values,
            where each DataFrame represents the data to be inserted into the corresponding table.
    Returns:
        None
    """
    # Must insert dim tables first to avoid missing foreign keys in fact tables
    try:
        for table_name in dataframes_dict:
            print(f"Inserting {table_name}")
            if "dim" in table_name:
                table_columns = dataframes_dict[table_name].columns.to_list()
                for index, row in dataframes_dict[table_name].iterrows():
                    columns_str = return_safe_sql_identifiers_str_from_list(
                        table_columns
                    )
                    values_str = return_safe_sql_literals_str_from_list(row.values)

                    # table_columns[0] must be primary key
                    sql_query = f"INSERT INTO {identifier(table_name)} ({columns_str}) VALUES ({(values_str)}) ON CONFLICT ({identifier(table_columns[0])}) DO UPDATE SET "
                    update_str = ", ".join(
                        [
                            f"{identifier(col)} = excluded.{identifier(col)}"
                            for col in table_columns
                        ]
                    )
                    sql_query += update_str
                    conn.run(sql_query)

        for table_name in dataframes_dict:
            print(f"Inserting {table_name}")
            if "fact" in table_name:
                table_columns = dataframes_dict[table_name].columns.to_list()
                for index, row in dataframes_dict[table_name].iterrows():
                    columns_str = return_safe_sql_identifiers_str_from_list(
                        table_columns
                    )
                    values_str = return_safe_sql_literals_str_from_list(row.values)

                    sql_query = f"INSERT INTO {identifier(table_name)} ({columns_str}) VALUES ({values_str})"
                    conn.run(sql_query)

    except exceptions.DatabaseError as e:
        print(e)
        print(f"Database error in {table_name}")
        print(dataframes_dict[table_name])
        print(f"SQL query: {sql_query}")
        raise e


def return_safe_sql_identifiers_str_from_list(list_of_identifiers: list) -> str:
    safe_identifiers_str = ""
    for index, value in enumerate(list_of_identifiers):
        if index == len(list_of_identifiers) - 1:
            str_to_add = identifier(value)
        else:
            str_to_add = f"{identifier(value)}, "
        safe_identifiers_str = safe_identifiers_str + str_to_add
    return safe_identifiers_str


def return_safe_sql_literals_str_from_list(list_of_literals: list) -> str:
    safe_literals_str = ""
    for index, value in enumerate(list_of_literals):
        if index == len(list_of_literals) - 1:
            str_to_add = literal(value)
        else:
            str_to_add = f"{literal(value)}, "
        safe_literals_str = safe_literals_str + str_to_add
    return safe_literals_str
