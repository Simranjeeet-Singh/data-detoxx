import pandas as pd
from pg8000 import Connection


def insert_dataframes_into_warehouse(
    conn: Connection, tables_data: dict[str, pd.DataFrame]
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
    for table in tables_data:
        table_columns = tables_data[table].columns.to_list()
        for index, row in tables_data[table].iterrows():
            columns_str = ", ".join(table_columns)
            values_str = ", ".join([f"'{value}'" for value in row.values])
            # Construct the SQL INSERT statement with ON CONFLICT clause
            if "fact" in table:
                sql_query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"
            else:
                sql_query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str}) ON CONFLICT ({table_columns[0]}) DO UPDATE SET "
                update_str = ", ".join(
                    [f"{col} = excluded.{col}" for col in table_columns]
                )
                sql_query += update_str
            conn.run(sql_query)
