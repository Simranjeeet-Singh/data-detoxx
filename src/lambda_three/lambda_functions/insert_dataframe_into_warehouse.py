import pandas as pd
from pg8000 import Connection


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
    for table_name in dataframes_dict:
        if "dim" in table_name:
            table_columns = dataframes_dict[table_name].columns.to_list()
            for index, row in dataframes_dict[table_name].iterrows():
                columns_str = ", ".join(table_columns)
                values_str = ", ".join([f"'{value}'" for value in row.values])

            # table_columns[0] must be primary key
            sql_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str}) ON CONFLICT ({table_columns[0]}) DO UPDATE SET "
            update_str = ", ".join([f"{col} = excluded.{col}" for col in table_columns])
            sql_query += update_str
            conn.run(sql_query)

    for table_name in dataframes_dict:
        if "fact" in table_name:
            table_columns = dataframes_dict[table_name].columns.to_list()
            for index, row in dataframes_dict[table_name].iterrows():
                columns_str = ", ".join(table_columns)
                values_str = ", ".join([f"'{value}'" for value in row.values])

            sql_query = (
                f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
            )
            conn.run(sql_query)
