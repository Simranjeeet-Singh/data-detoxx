from pg8000.native import Connection, identifier, literal
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import os

def extract_tablenames(conn: Connection) -> list[str]:
    """
    Parameters:
      -conn: pg8000.native Connection object to a SQL db.
    Returns:
      -Names of all its tables in a list.
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
    -table_name: name of table in schema
    -counter: counter for the number of times data have been downloaded
    -last_updated: timestamp for the most recent row that has been pulled from the SQL
    Returns:
    -path to .csv file containing the downloaded data in format:
    '/{table_name}/{table_name}_[#{counter}]_{last_date_converted}.csv'
    '''
    return f'./{table_name}/{table_name}_[#{counter}]_{last_updated}.csv'

def extract_last_date(conn: Connection, table_name: str) -> datetime:
    '''
    Parameters:
    -conn: pg8000.native Connection object to a SQL db.
    -table_name: name of table in schema
    Returns:
    - most recent last_updated value
    '''
    last_date = conn.run(f'''SELECT last_updated FROM {identifier(table_name)}
                    ORDER BY last_updated DESC
                    LIMIT 1
                    ;''')
    return last_date[0][0]

def save_table_to_csv(conn: Connection, table_name: str, last_date, counter: int) -> None:
    """
    Parameters:
      -conn: pg8000.native Connection object to a SQL db;
      -table_name: str representing the name of one of its tables.
      -last_date: timestamp representing the latest date that has been written to a .csv file
      -counter: the current iteration of the program
    Returns:
      -None
    This function stores rows of the given table_name in a pandas dataframe and saves it to table_name.csv.
    Rows are ordered by the column last_updated, with the most recent date at the end.
    If there are no rows, it does nothing.
    """
    last_date_converted=convert_to_utc(extract_last_date(conn, table_name))
    rows = conn.run(f'''SELECT * FROM {identifier(table_name)}
                    WHERE last_updated > {literal(last_date)}
                    ORDER BY last_updated ASC
                    ;''')
    if rows:
      cols_name = [el["name"] for el in conn.columns]
      df = pd.DataFrame(rows)
      df.index = df[0].values
      df.columns = cols_name
      df.to_csv(path_to_csv(table_name,counter,last_date_converted), sep=",", index=False, encoding="utf-8")

def convert_to_utc(datetime: datetime) -> str:
    """
    Convert a date-time string to a UTC format string.

    Args:
        datetime_str (str): A string representing date and time in the format 'YYYY-MM-DD HH:MM:SS.SSS'.

    Returns:
        str: A string representing date and time in UTC format 'YYYY-MM-DDTHHMMSS.SSSZ'.
    """
    # dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    utc_format_str = datetime.strftime('%Y-%m-%dT%H%M%S%f')[:-3] + 'Z'
    return utc_format_str


def save_db_to_csv() -> None:
    """
    Parameters:
    -None
    Returns:
    -None
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
        save_table_to_csv(conn, table_name,'2024-02-13 18:19:09.733',0)
    conn.close()


if __name__ == "__main__":
    save_db_to_csv()
    
