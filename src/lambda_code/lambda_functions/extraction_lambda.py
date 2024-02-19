from pg8000.native import Connection, identifier, literal
import pandas as pd
from datetime import datetime
from lambda_functions.utils.date_utils import convert_datetime_to_utc
from lambda_functions.utils.utils import (
    list_files_from_s3,
    return_latest_counter_and_timestamp_from_filenames,
)
from pathlib import Path


def extract_tablenames(conn: Connection) -> list[str]:
    """
    Parameters:
    - conn: pg8000.native Connection object to a SQL db.

    Returns:
    - Names of all its tables in a list.
    """
    sql_query_tablenames = """SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    AND table_type='BASE TABLE';"""
    return [
        el[0] for el in conn.run(sql_query_tablenames) if el[0] != "_prisma_migrations"
    ]


def path_to_csv(table_name: str, counter: int, last_updated: datetime) -> str:
    """
    Parameters:
    - table_name: name of table in schema
    - counter: counter for the number of times data have been downloaded
    - last_updated: timestamp for the most recent row that has been pulled from SQL

    Returns:
    - path to .csv file containing the downloaded data in format:
    '{table_name}_[#{counter}]_{last_date_converted}.csv'
    """
    return f"{table_name}/{table_name}__[#{counter}]__{last_updated}.csv"


def extract_last_updated_from_table(conn: Connection, table_name: str) -> datetime:
    """
    Parameters:
    - conn: pg8000.native Connection object to a SQL db.
    - table_name: name of table in schema

    Returns:
    - most recent last_updated value in the table
    """
    last_timestamp = conn.run(
        f"""SELECT last_updated FROM {identifier(table_name)}
                    ORDER BY last_updated DESC
                    LIMIT 1
                    ;"""
    )
    return last_timestamp[0][0]


def save_table_to_csv(cols_name: list, rows: list[list], path: str, logger) -> None:
    if rows:
        df = pd.DataFrame(rows)
        df.index = df[0].values
        df.columns = cols_name
        df.to_csv(f"/tmp/{path}", sep=",", index=False, encoding="utf-8")
        logger.info(f"Wrote {len(rows)} to file {path}")


def save_db_to_csv(conn: Connection, logger, bucket_name: str) -> list:
    """
    Parameters:
    - conn: pg8000 connection to SQL db

    Returns:
    - List of the paths of the newly written .csv files

    Connects to a server specified in the .env variable via pg8000.native;
    Extract all rows from all its SQL tables;
    Inputs them in pandas dataframes;
    Saves each dataframe to .csv files with same name as table;
    returns the paths of these .csv files.
    """

    tablenames = extract_tablenames(conn)
    new_csv_paths = []
    filenames = list_files_from_s3(bucket_name)
    for table_name in tablenames:
        last_updated_from_database_utc_timestamp = convert_datetime_to_utc(
            extract_last_updated_from_table(conn, table_name)
        )
        counter, last_updated_from_ingestion_bucket_sql_timestamp = (
            return_latest_counter_and_timestamp_from_filenames(table_name, filenames)
        )
        if counter == 0:
            rows = conn.run(
                f"""SELECT * FROM {identifier(table_name)}
                    ORDER BY last_updated ASC
                    ;"""
            )
        else:
            rows = conn.run(
                f"""SELECT * FROM {identifier(table_name)}
                    WHERE last_updated > {literal(last_updated_from_ingestion_bucket_sql_timestamp)}
                    ORDER BY last_updated ASC
                    ;"""
            )
        cols_name = [el["name"] for el in conn.columns]
        path = path_to_csv(
            table_name,
            counter + 1,
            last_updated_from_database_utc_timestamp,
        )
        folder_name = Path(f"/tmp/{table_name}").mkdir(parents=True, exist_ok=True)
        new_csv_paths.append(path)
        save_table_to_csv(cols_name, rows, path, logger)
    return new_csv_paths


if __name__ == "__main__":
    save_db_to_csv()
