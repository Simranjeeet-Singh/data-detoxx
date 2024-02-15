from pg8000.native import Connection, identifier, literal
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import os

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

def path_to_csv(table_name: str,counter: int,last_updated: datetime) -> str:
    '''
    Parameters:
    - table_name: name of table in schema
    - counter: counter for the number of times data have been downloaded
    - last_updated: timestamp for the most recent row that has been pulled from SQL

    Returns:
    - path to .csv file containing the downloaded data in format:
    '/{table_name}/{table_name}_[#{counter}]_{last_date_converted}.csv'
    '''
    return f'./{table_name}/{table_name}_[#{counter}]_{last_updated}.csv'

def extract_last_timestamp_from_table(conn: Connection, table_name: str) -> datetime:
    '''
    Parameters:
    - conn: pg8000.native Connection object to a SQL db.
    - table_name: name of table in schema

    Returns:
    - most recent last_updated value in the table
    '''
    last_timestamp = conn.run(f'''SELECT last_updated FROM {identifier(table_name)}
                    ORDER BY last_updated DESC
                    LIMIT 1
                    ;''')
    return last_timestamp[0][0]

def save_table_to_csv(cols_name: list, rows: list[list], path: str) -> None:
    if rows:
        df = pd.DataFrame(rows)
        df.index = df[0].values
        df.columns = cols_name
        df.to_csv(path, sep=",", index=False, encoding="utf-8")


def convert_to_utc(datetime: datetime) -> str:
    """
    Convert a date-time string to a UTC format string.

    Args:
    - datetime_str (str): A string representing date and time in the format 'YYYY-MM-DD HH:MM:SS.SSS'.

    Returns:
    - str: A string representing date and time in UTC format 'YYYY-MM-DDTHHMMSS.SSSZ'.
    """
    utc_format_str = datetime.strftime('%Y-%m-%dT%H%M%S%f')[:-3] + 'Z'
    return utc_format_str


def save_db_to_csv() -> None:
    """
    Parameters:
    - None

    Returns:
    - None

    Connects to a server specified in the .env variable via pg8000.native;
    Extract all rows from all its SQL tables;
    Inputs them in pandas dataframes;
    Saves each dataframe to .csv files with same name as table;
    """
    load_dotenv()
    conn = Connection(
        host=os.environ["Hostname"],
        user=os.environ["Username"],
        password=os.environ["Password"],
        database=os.environ["Database_name"],
        port=os.environ["Port"],
    )
    tablenames = extract_tablenames(conn)
    for table_name in tablenames:
        last_updated_from_database_converted=convert_to_utc(extract_last_timestamp_from_table(conn, table_name))
        rows = conn.run(f'''SELECT * FROM {identifier(table_name)}
                    WHERE last_updated > {literal(last_date_from_other_function)}
                    ORDER BY last_updated ASC
                    ;''')
        cols_name = [el["name"] for el in conn.columns]
        path=path_to_csv(table_name,counter_from_other_function,last_updated_from_database_converted)
        save_table_to_csv(cols_name, rows, path)
    conn.close()


if __name__ == "__main__":
    save_db_to_csv()
    
